from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from .email_backend import EmailBackend
from django.contrib import messages
from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.


def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("adminDashboard"))
        else:
            return redirect(reverse("voting:voterDashboard"))

    context = {}
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                if user.user_type == '1':
                    return JsonResponse({'redirect': reverse("adminDashboard")})
                else:
                    return JsonResponse({'redirect': reverse("voting:voterDashboard")})
            else:
                if user.user_type == '1':
                    return redirect(reverse("adminDashboard"))
                else:
                    return redirect(reverse("voting:voterDashboard"))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid email or password'}, status=400)
            else:
                messages.error(request, "Invalid email or password")
                return redirect(reverse("account:login"))

    return render(request, "voting/login.html", context)


def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None, request.FILES or None)
    context = {
        'form1': userForm,
        'form2': voterForm
    }
    
    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            voter = voterForm.save(commit=False)
            voter.admin = user
            user.save()
            voter.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Account created successfully! You can now log in.'
                })
            
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('account:login')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Form validation failed',
                    'errors': {
                        'user_form': userForm.errors,
                        'voter_form': voterForm.errors
                    }
                }, status=400)
            
            messages.error(request, "Provided data failed validation")
            return render(request, "voting/register.html", context)

    return render(request, "voting/register.html", context)


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account:login"))

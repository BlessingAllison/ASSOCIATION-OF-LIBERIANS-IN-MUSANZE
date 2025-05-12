from django.shortcuts import render, redirect, reverse, resolve_url
from django.http import JsonResponse, HttpResponseRedirect
from .email_backend import EmailBackend
from django.contrib import messages
from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.


def account_login(request):
    # If user is already logged in, redirect to appropriate dashboard
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect('administrator:adminDashboard')
        else:
            return redirect('voting:voterDashboard')

    context = {}
    next_url = request.GET.get('next', '')
    
    # Prevent redirect loops by checking if next is a login URL
    if next_url and (next_url == reverse('account:login') or next_url.startswith(reverse('account:login') + '?')):
        next_url = ''
    
    if request.method == 'POST':
        user = EmailBackend.authenticate(
            request, 
            username=request.POST.get('email'), 
            password=request.POST.get('password')
        )
        
        if user is not None:
            login(request, user)
            post_next = request.POST.get('next', '')
            
            # Determine the best redirect URL
            if post_next and post_next != reverse('account:login') and not post_next.startswith(reverse('account:login') + '?'):
                next_url = post_next
            elif next_url and next_url != reverse('account:login') and not next_url.startswith(reverse('account:login') + '?'):
                next_url = next_url
            else:
                next_url = None
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                if next_url:
                    return JsonResponse({'redirect': next_url})
                if user.user_type == '1':
                    return JsonResponse({'redirect': reverse('administrator:adminDashboard')})
                else:
                    return JsonResponse({'redirect': reverse('voting:voterDashboard')})
            else:
                if next_url:
                    return redirect(next_url)
                if user.user_type == '1':
                    return redirect('administrator:adminDashboard')
                else:
                    return redirect('voting:voterDashboard')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid email or password'}, status=400)
            else:
                messages.error(request, "Invalid email or password")
    
    # For GET requests, include the 'next' parameter in the context
    context['next'] = next_url
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

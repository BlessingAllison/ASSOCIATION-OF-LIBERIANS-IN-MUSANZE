from django.shortcuts import render, redirect
from django.urls import reverse
from account.views import account_login

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse('account:login'))
    context = {}
    # return render(request, "voting/login.html", context)

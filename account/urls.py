from django.urls import path, re_path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.account_login, name="login"),
    re_path(r'^register/?$', views.account_register, name="register"),
    re_path(r'^logout/?$', views.account_logout, name="logout"),
]

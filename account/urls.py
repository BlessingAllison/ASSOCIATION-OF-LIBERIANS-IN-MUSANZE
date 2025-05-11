from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.account_login, name="login"),
    path('register/', views.account_register, name="register"),
    path('logout/', views.account_logout, name="logout"),
]

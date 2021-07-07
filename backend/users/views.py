from django.contrib.auth.views import LoginView
from django.shortcuts import render  # noqa


# Create your views here.
class UserLoginView(LoginView):
    redirect_field_name = "home"
    redirect_authenticated_user = True
    template_name = "registration/login.html"

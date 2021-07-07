from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render  # noqa
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegisterForm
from users.models import User


class UserLoginView(LoginView):
    redirect_field_name = "home"
    redirect_authenticated_user = True
    template_name = "registration/login.html"


class SignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "registration/signup.html"
    success_message = "Your profile was created successfully"
    success_url = reverse_lazy("home")

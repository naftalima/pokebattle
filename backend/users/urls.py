from django.conf.urls import include
from django.urls import path

from .views import SignUpView, UserLoginView


urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("oauth/", include("social_django.urls"), name="social"),
]

from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import SignUpView, UserLoginView


urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("oauth/", include("social_django.urls"), name="social"),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"),
        name="password_change",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

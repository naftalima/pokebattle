from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string

from users.models import User


def create_guest_opponent(opponent_email):
    opponent = User.objects.create(email=opponent_email)
    random_password = get_random_string(length=64)
    opponent.set_password(random_password)
    opponent.save()
    return opponent


def invite_unregistered_opponent(opponent):
    invite_form = PasswordResetForm(data={"email": opponent.email})
    invite_form.is_valid()
    invite_form.save(
        subject_template_name="registration/invite_signup_subject.txt",
        email_template_name="registration/invite_signup_email.html",
        from_email=settings.EMAIL_ADDRESS,
        html_email_template_name=None,
        domain_override=settings.HOST,
    )

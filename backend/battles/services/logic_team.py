from django.utils.crypto import get_random_string

from users.models import User


def create_guest_opponent(opponent_email):
    opponent = User.objects.create(email=opponent_email)
    random_password = get_random_string(length=64)
    opponent.set_password(random_password)
    opponent.save()
    return opponent

from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string

from battles.models import TeamPokemon
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


def all_teams_has_pokemons(battle):
    creator_team_has_pokemons = TeamPokemon.objects.filter(
        team__trainer=battle.creator, team__battle=battle
    ).exists()
    opponent_team_has_pokemons = TeamPokemon.objects.filter(
        team__trainer=battle.opponent, team__battle=battle
    ).exists()
    teams_are_complete = creator_team_has_pokemons and opponent_team_has_pokemons
    return teams_are_complete

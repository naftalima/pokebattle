from django.conf import settings

from templated_email import send_templated_mail

from battles.services.logic_battle import get_pokemons  # pylint: disable=import-error
from battles.utils.format import get_username  # pylint: disable=import-error


def email_battle_result(battle):
    send_templated_mail(
        template_name="battle_result",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "winner_username": get_username(battle.winner.email),
            "creator_username": get_username(battle.creator.email),
            "opponent_username": get_username(battle.opponent.email),
            "creator_pokemon_team": get_pokemons(battle)["creator"],
            "opponent_pokemon_team": get_pokemons(battle)["opponent"],
        },
    )


def email_invite(battle):
    send_templated_mail(
        template_name="invite",
        from_email=settings.EMAIL_ADDRESS,
        recipient_list=[battle.opponent.email],
        context={
            "creator_username": get_username(battle.creator.email),
            "opponent_username": get_username(battle.opponent.email),
        },
    )

from templated_email import send_templated_mail

from battles.services.logic_battle import get_pokemons  # pylint: disable=import-error
from battles.utils.format import get_username  # pylint: disable=import-error


def email_battle_result(battle):
    send_templated_mail(
        template_name="battle_result",
        from_email="nathalia.lima@vinta.com.br",
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "winner": get_username(battle.winner.email),
            "creator": get_username(battle.creator.email),
            "opponent": get_username(battle.opponent.email),
            "creator_pokemon_team": get_pokemons(battle)["creator"],
            "opponent_pokemon_team": get_pokemons(battle)["opponent"],
        },
    )

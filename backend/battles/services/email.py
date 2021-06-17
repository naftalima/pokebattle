from templated_email import send_templated_mail

from battles.services.logic_battle import get_pokemons


def email_battle_result(battle):
    send_templated_mail(
        template_name="battle_result",
        from_email="nathalia.lima@vinta.com.br",
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "winner": battle.winner,
            "creator": battle.creator,
            "opponent": battle.opponent,
            "creator_pokemon_team": get_pokemons(battle)["creator"],
            "opponent_pokemon_team": get_pokemons(battle)["opponent"],
        },
    )

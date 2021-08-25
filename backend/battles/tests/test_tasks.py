from unittest import mock

from django.conf import settings

from model_bakery import baker

from battles.models import Battle, TeamPokemon
from battles.services.logic_battle import get_pokemons
from battles.tasks import run_battle_and_send_result
from battles.utils.format import get_username  # pylint: disable=import-error
from common.utils.tests import TestCaseUtils


class RunAsyncBattleTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.creator = self.user
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battles.Battle", creator=self.creator, opponent=self.opponent)
        self.team_creator = baker.make("battles.Team", battle=self.battle, trainer=self.creator)
        self.team_opponent = baker.make("battles.Team", battle=self.battle, trainer=self.opponent)
        self.pokemons = [baker.make("pokemons.Pokemon") for i in range(1, 4)]

    @mock.patch("battles.services.email.send_templated_mail")
    def test_run_battle_and_send_result(self, email_mock):

        add_pokemons_to_team(pokemons=self.pokemons, positions=[1, 2, 3], team=self.team_creator)
        add_pokemons_to_team(pokemons=self.pokemons, positions=[3, 2, 1], team=self.team_opponent)

        run_battle_and_send_result(self.battle.id)

        battle = Battle.objects.filter(creator=self.creator, opponent=self.opponent)[0]

        self.assertTrue(battle.winner)

        email_mock.assert_called_with(
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


def add_pokemons_to_team(pokemons, positions, team):
    for pokemon, position in zip(pokemons, positions):
        TeamPokemon.objects.create(team=team, pokemon=pokemon, order=position)

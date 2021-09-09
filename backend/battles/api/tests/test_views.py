import json
from unittest import mock

from django.urls import reverse

from model_bakery import baker

from common.utils.tests import TestCaseUtils


class BattleListTests(TestCaseUtils):
    view_name = "api:battle_list"

    def setUp(self):
        super().setUp()
        self.view_url = reverse(self.view_name)

    def test_return_200_when_accessing_endpoint(self):
        response = self.auth_client.get(self.view_url)
        self.assertResponse200(response)

    def test_return_queryset(self):
        battle = baker.make("battles.Battle", creator=self.user)
        response = self.auth_client.get(self.view_url)
        self.assertTrue(response.data)

        self.assertEqual(response.data[0].get("id"), battle.id)

    def test_return_empty_queryset(self):
        """ """
        baker.make("battles.Battle")
        response = self.auth_client.get(self.view_url)
        self.assertFalse(response.data)


class SelectTeamTests(TestCaseUtils):
    view_name = "api:team_edit"

    def setUp(self):
        super().setUp()
        self.creator = self.user
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battles.Battle", creator=self.creator, opponent=self.opponent)
        self.team_creator = baker.make("battles.Team", battle=self.battle, trainer=self.creator)
        self.team_opponent = baker.make("battles.Team", battle=self.battle, trainer=self.opponent)
        self.view_url = reverse(self.view_name, kwargs={"pk": self.team_creator.pk})
        baker.make("pokemons.Pokemon", name="pikachu")
        baker.make("pokemons.Pokemon", name="eevee")
        baker.make("pokemons.Pokemon", name="nidorina")

    @mock.patch("battles.services.api_integration.check_pokemons_exists_in_pokeapi")
    def test_update_team_correct(
        self, mock_check_pokemons_exists_in_pokeapi
    ):  # pylint: disable=unused-argument
        team_pokemon_data = {
            "pokemon_1": "pikachu",
            "position_1": 1,
            "pokemon_2": "eevee",
            "position_2": 2,
            "pokemon_3": "nidorina",
            "position_3": 3,
        }

        response = self.auth_client.patch(
            self.view_url, json.dumps(team_pokemon_data), content_type="application/json"
        )
        self.assertResponse200(response)

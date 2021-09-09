import json
from unittest import mock

from django.conf import settings
from django.urls import reverse

from model_bakery import baker

from battles.models import Battle, TeamPokemon
from battles.services.logic_battle import get_pokemons
from battles.utils.format import get_username  # pylint: disable=import-error
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


class BattleDetailTest(TestCaseUtils):
    view_name = "api:battle_detail"

    def setUp(self):
        super().setUp()
        self.creator = self.user
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battles.Battle", creator=self.creator, opponent=self.opponent)
        self.team_creator = baker.make("battles.Team", battle=self.battle, trainer=self.creator)
        self.team_opponent = baker.make("battles.Team", battle=self.battle, trainer=self.opponent)
        self.view_url = reverse(self.view_name, kwargs={"pk": self.battle.pk})

    def test_return_200_when_accessing_endpoint(self):
        response = self.auth_client.get(self.view_url)
        self.assertResponse200(response)

    def test_return_forbidden(self):
        self.auth_client.logout()
        response = self.auth_client.get(self.view_url)
        self.assertResponse403(response)


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
        self.team_pokemon = None
        baker.make("pokemons.Pokemon", name="pikachu")
        baker.make("pokemons.Pokemon", name="eevee")
        baker.make("pokemons.Pokemon", name="nidorina")

    @mock.patch("battles.services.api_integration.get_pokemon_from_api")
    def test_update_team_correct(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "pikachu":
                fake_json = {
                    "defense": 65,
                    "attack": 45,
                    "hp": 35,
                    "name": "pikachu",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 179,
                }
            elif pokemon_name == "eevee":
                fake_json = {
                    "defense": 55,
                    "attack": 45,
                    "hp": 15,
                    "name": "eevee",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "nidorina":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "nidorina",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

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

        team_pokemon = TeamPokemon.objects.filter(team=self.team_creator)
        self.assertTrue(team_pokemon)

    @mock.patch("battles.services.api_integration.get_pokemon_from_api")
    def test_update_repetead_pokemons(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "pikachu":
                fake_json = {
                    "defense": 65,
                    "attack": 45,
                    "hp": 35,
                    "name": "pikachu",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 179,
                }
            elif pokemon_name == "eevee":
                fake_json = {
                    "defense": 55,
                    "attack": 45,
                    "hp": 15,
                    "name": "eevee",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "nidorina":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "nidorina",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

        team_pokemon_data = {
            "pokemon_1": "pikachu",
            "position_1": 1,
            "pokemon_2": "pikachu",
            "position_2": 2,
            "pokemon_3": "pikachu",
            "position_3": 3,
        }

        self.auth_client.patch(
            self.view_url, json.dumps(team_pokemon_data), content_type="application/json"
        )
        self.assertRaisesMessage(
            ValueError, "ERROR: Has repeated pokemon. Please select unique pokemons."
        )

        team_pokemon = TeamPokemon.objects.filter(team=self.team_creator)
        self.assertFalse(team_pokemon)

    @mock.patch("battles.services.api_integration.get_pokemon_from_api")
    def test_user_is_not_the_team_trainer(self, mock_get_pokemon):
        view_url = reverse(self.view_name, kwargs={"pk": self.team_opponent.pk})

        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "pikachu":
                fake_json = {
                    "defense": 65,
                    "attack": 45,
                    "hp": 35,
                    "name": "pikachu",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 179,
                }
            elif pokemon_name == "eevee":
                fake_json = {
                    "defense": 55,
                    "attack": 45,
                    "hp": 15,
                    "name": "eevee",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "nidorina":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "nidorina",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

        team_pokemon_data = {
            "pokemon_1": "pikachu",
            "position_1": 1,
            "pokemon_2": "pikachu",
            "position_2": 2,
            "pokemon_3": "pikachu",
            "position_3": 3,
        }

        self.auth_client.patch(
            view_url, json.dumps(team_pokemon_data), content_type="application/json"
        )

        team_pokemon = TeamPokemon.objects.filter(team=self.team_creator)
        self.assertFalse(team_pokemon)

    @mock.patch("battles.services.email.send_templated_mail")
    def test_send_battle_result(self, email_mock):
        pokemon_1 = baker.make("pokemons.Pokemon")
        pokemon_2 = baker.make("pokemons.Pokemon")
        pokemon_3 = baker.make("pokemons.Pokemon")

        self.team_pokemon = baker.make(
            "battles.TeamPokemon", team=self.team_opponent, pokemon=pokemon_1, order=1
        )
        self.team_pokemon = baker.make(
            "battles.TeamPokemon", team=self.team_opponent, pokemon=pokemon_2, order=2
        )
        self.team_pokemon = baker.make(
            "battles.TeamPokemon", team=self.team_opponent, pokemon=pokemon_3, order=3
        )

        team_pokemon_data = {
            "pokemon_1": "pikachu",
            "position_1": 1,
            "pokemon_2": "eevee",
            "position_2": 2,
            "pokemon_3": "nidorina",
            "position_3": 3,
        }
        self.auth_client.post(
            reverse(
                "battle-team-pokemons",
                kwargs={
                    "pk": self.team_creator.id,
                },
            ),
            team_pokemon_data,
            follow=True,
        )

        battle = Battle.objects.filter(creator=self.creator, opponent=self.opponent)[0]

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

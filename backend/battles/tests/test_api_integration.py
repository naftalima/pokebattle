from unittest import mock

from django.conf import settings
from django.urls import reverse

from model_bakery import baker

from battles.models import Battle
from battles.services.api_integration import check_pokemons_exists, get_pokemon_info
from battles.services.logic_battle import get_pokemons  # pylint: disable=import-error
from battles.services.logic_team_pokemon import check_team_sum_valid
from battles.utils.format import get_username  # pylint: disable=import-error
from common.utils.tests import TestCaseUtils


class PokeApiTest(TestCaseUtils):
    @mock.patch("battles.services.api_integration.get_pokemon_info")
    def test_valid_pokemon_team(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "mareep":
                fake_json = {
                    "defense": 65,
                    "attack": 45,
                    "hp": 35,
                    "name": "mareep",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "pokemon_id": 179,
                }
            elif pokemon_name == "cleffa":
                fake_json = {
                    "defense": 55,
                    "attack": 45,
                    "hp": 15,
                    "name": "cleffa",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "pokemon_id": 173,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "pokemon_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func
        pokemon_names = ["mareep", "cleffa", "bulbasaur"]

        pokemons_data = [get_pokemon_info(pokemon_name) for pokemon_name in pokemon_names]

        is_team_sum_valid = check_team_sum_valid(pokemons_data)

        self.assertTrue(is_team_sum_valid)

    @mock.patch("battles.services.api_integration.get_response")
    def test_invalid_pokemon_name(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = None
            if pokemon_name == "mareep":
                fake_json = {
                    "defense": 65,
                    "attack": 45,
                    "hp": 35,
                    "name": "mareep",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "pokemon_id": 179,
                }
            elif pokemon_name == "cleffa":
                fake_json = {
                    "defense": 55,
                    "attack": 45,
                    "hp": 15,
                    "name": "cleffa",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "pokemon_id": 173,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "pokemon_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

        pokemon_names = ["pikachuuuur", "cleffa", "bulbasaur"]

        is_pokemons_valid = check_pokemons_exists(pokemon_names)

        self.assertFalse(is_pokemons_valid)


class SendInviteMailTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")

    @mock.patch("battles.services.email.send_templated_mail")
    def test_send_email_invite(self, email_mock):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.opponent.email,
        }

        self.auth_client.post(reverse("battle-opponent"), battle_data)

        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)[0]

        email_mock.assert_called_with(
            template_name="invite",
            from_email=settings.EMAIL_ADDRESS,
            recipient_list=[battle.opponent.email],
            context={
                "creator_username": get_username(battle.creator.email),
                "opponent_username": get_username(battle.opponent.email),
            },
        )


class SendResultMailTest(TestCaseUtils):  # pylint: disable=too-many-instance-attributes
    def setUp(self):
        super().setUp()
        self.creator = self.user
        self.opponent = baker.make("users.User")

        self.battle = baker.make("battles.Battle", creator=self.creator, opponent=self.opponent)
        self.team_creator = baker.make("battles.Team", battle=self.battle, trainer=self.creator)
        self.team_opponent = baker.make("battles.Team", battle=self.battle, trainer=self.opponent)

        self.pokemon_1 = baker.make("pokemons.Pokemon")
        self.pokemon_2 = baker.make("pokemons.Pokemon")
        self.pokemon_3 = baker.make("pokemons.Pokemon")

        self.team_pokemon = baker.make(
            "battles.TeamPokemon", team=self.team_opponent, pokemon=self.pokemon_1, order=1
        )
        self.team_pokemon = baker.make(
            "battles.TeamPokemon", team=self.team_opponent, pokemon=self.pokemon_2, order=2
        )
        self.team_pokemon = baker.make(
            "battles.TeamPokemon", team=self.team_opponent, pokemon=self.pokemon_3, order=3
        )

    @mock.patch("battles.services.email.send_templated_mail")
    def test_send_battle_result(self, email_mock):

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

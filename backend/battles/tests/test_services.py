from unittest import mock

from django.conf import settings
from django.urls import reverse

from model_bakery import baker

from battles.models import Battle, TeamPokemon
from battles.services.api_integration import (
    check_pokemons_exists_in_pokeapi,
    get_or_create_pokemon,
    get_pokemon_info,
)
from battles.services.logic_battle import get_pokemons, get_winner
from battles.services.logic_team_pokemon import (
    check_pokemons_unique,
    check_position_unique,
    check_team_sum_valid,
)
from battles.utils.format import get_username  # pylint: disable=import-error
from common.utils.tests import TestCaseUtils


class PokeApiTest(TestCaseUtils):
    @mock.patch("battles.services.api_integration.get_pokemon_from_api")
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
                    "poke_id": 179,
                }
            elif pokemon_name == "cleffa":
                fake_json = {
                    "defense": 55,
                    "attack": 45,
                    "hp": 15,
                    "name": "cleffa",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func
        pokemon_names = ["mareep", "cleffa", "bulbasaur"]

        pokemons_data = [get_pokemon_info(pokemon_name) for pokemon_name in pokemon_names]

        is_team_sum_valid = check_team_sum_valid(pokemons_data)

        self.assertTrue(is_team_sum_valid)

    @mock.patch("battles.services.api_integration.get_pokemon_from_api")
    def test_invalid_pokemon_team(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "venusaur":
                fake_json = {
                    "defense": 165,
                    "attack": 145,
                    "hp": 235,
                    "name": "venusaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 179,
                }
            elif pokemon_name == "ivysaur":
                fake_json = {
                    "defense": 255,
                    "attack": 145,
                    "hp": 150,
                    "name": "ivysaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 120,
                    "attack": 100,
                    "hp": 200,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

        pokemon_names = ["bulbasaur", "ivysaur", "venusaur"]

        pokemons_data = [get_pokemon_info(pokemon_name) for pokemon_name in pokemon_names]

        is_team_sum_valid = check_team_sum_valid(pokemons_data)

        self.assertFalse(is_team_sum_valid)

    @mock.patch("battles.services.api_integration.get_pokemon_from_api")
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
                    "poke_id": 179,
                }
            elif pokemon_name == "cleffa":
                fake_json = {
                    "defense": 55,
                    "attack": 45,
                    "hp": 15,
                    "name": "cleffa",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

        pokemon_names = ["pikachuuuur", "cleffa", "bulbasaur"]

        is_pokemons_valid = check_pokemons_exists_in_pokeapi(pokemon_names)

        self.assertFalse(is_pokemons_valid)

    @mock.patch("battles.services.api_integration.get_pokemon_from_api")
    def test_valid_pokemons(self, mock_get_pokemon):
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
                    "poke_id": 179,
                }
            elif pokemon_name == "cleffa":
                fake_json = {
                    "defense": 55,
                    "attack": 45,
                    "hp": 15,
                    "name": "cleffa",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

        pokemon_names = ["mareep", "cleffa", "bulbasaur"]

        is_pokemons_valid = check_pokemons_exists_in_pokeapi(pokemon_names)

        self.assertTrue(is_pokemons_valid)


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


class LogicTeamPokemonTest(TestCaseUtils):
    def test_position_unique(self):
        positions = [1, 2, 3]
        is_positions_unique = check_position_unique(positions)
        self.assertTrue(is_positions_unique)

    def test_position_repeated(self):
        positions = [1, 2, 2]
        is_positions_unique = check_position_unique(positions)
        self.assertFalse(is_positions_unique)

    def test_pokemons_unique(self):
        pokemon_names = ["pikachu", "eevee", "nidorina"]
        is_pokemons_unique = check_pokemons_unique(pokemon_names)
        self.assertTrue(is_pokemons_unique)

    def test_pokemons_repeated(self):
        pokemon_names = ["pikachu", "pikachu", "pikachu"]
        is_pokemons_unique = check_pokemons_unique(pokemon_names)
        self.assertFalse(is_pokemons_unique)

    @mock.patch("battles.services.api_integration.get_pokemon_info")
    def test_team_sum_valid(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "nidorina":
                fake_json = {
                    "defense": 65,
                    "attack": 45,
                    "hp": 35,
                    "name": "nidorina",
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
            elif pokemon_name == "pikachu":
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": "pikachu",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

        pokemon_names = ["pikachu", "eevee", "nidorina"]
        pokemons_data = [get_pokemon_info(pokemon_name) for pokemon_name in pokemon_names]
        is_team_sum_valid = check_team_sum_valid(pokemons_data)
        self.assertTrue(is_team_sum_valid)

    @mock.patch("battles.services.api_integration.get_pokemon_info")
    def test_team_sum_invalid(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "venusaur":
                fake_json = {
                    "defense": 165,
                    "attack": 145,
                    "hp": 235,
                    "name": "venusaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 179,
                }
            elif pokemon_name == "ivysaur":
                fake_json = {
                    "defense": 255,
                    "attack": 145,
                    "hp": 150,
                    "name": "ivysaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 120,
                    "attack": 100,
                    "hp": 200,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func

        pokemon_names = ["bulbasaur", "ivysaur", "venusaur"]
        pokemons_data = [get_pokemon_info(pokemon_name) for pokemon_name in pokemon_names]
        is_team_sum_valid = check_team_sum_valid(pokemons_data)
        self.assertFalse(is_team_sum_valid)


class LogicBattleTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.creator = self.user
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battles.Battle", creator=self.creator, opponent=self.opponent)
        self.team_creator = baker.make("battles.Team", battle=self.battle, trainer=self.creator)
        self.team_opponent = baker.make("battles.Team", battle=self.battle, trainer=self.opponent)
        self.pokemons = [baker.make("pokemons.Pokemon") for i in range(1, 4)]

    def add_pokemons_to_team(self, pokemons, positions, team):
        for pokemon, position in zip(pokemons, positions):
            TeamPokemon.objects.create(team=team, pokemon=pokemon, order=position)

    @mock.patch("battles.services.api_integration.get_pokemon_info")
    def test_get_winner_and_opponent_won(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "venusaur":
                fake_json = {
                    "defense": 165,
                    "attack": 145,
                    "hp": 235,
                    "name": "venusaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 179,
                }
            elif pokemon_name == "ivysaur":
                fake_json = {
                    "defense": 255,
                    "attack": 145,
                    "hp": 150,
                    "name": "ivysaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 120,
                    "attack": 100,
                    "hp": 200,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 132,
                }
            elif pokemon_name == "ditto":
                fake_json = {
                    "defense": 48,
                    "attack": 48,
                    "hp": 48,
                    "name": "ditto",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func
        pokemon_names = ["bulbasaur", "ivysaur", "venusaur", "ditto"]
        pokemons = [
            get_or_create_pokemon(pokemon_data=get_pokemon_info(pokemon_name=pokemon_name))
            for pokemon_name in pokemon_names
        ]

        creator_pkns = pokemons[1:]
        opponent_pkns = pokemons[0:3]

        self.add_pokemons_to_team(
            pokemons=creator_pkns, positions=[1, 2, 3], team=self.team_creator
        )
        self.add_pokemons_to_team(
            pokemons=opponent_pkns, positions=[3, 2, 1], team=self.team_opponent
        )
        winner = get_winner(self.battle)
        self.assertTrue(winner)
        self.assertEqual(winner, self.opponent)

    @mock.patch("battles.services.api_integration.get_pokemon_info")
    def test_get_winner_and_creator_won(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == "venusaur":
                fake_json = {
                    "defense": 165,
                    "attack": 145,
                    "hp": 235,
                    "name": "venusaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 179,
                }
            elif pokemon_name == "ivysaur":
                fake_json = {
                    "defense": 255,
                    "attack": 145,
                    "hp": 150,
                    "name": "ivysaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 173,
                }
            elif pokemon_name == "bulbasaur":
                fake_json = {
                    "defense": 120,
                    "attack": 100,
                    "hp": 200,
                    "name": "bulbasaur",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            elif pokemon_name == "ditto":
                fake_json = {
                    "defense": 48,
                    "attack": 48,
                    "hp": 48,
                    "name": "ditto",
                    "img_url": "https://raw.githubusercontent.com"
                    "/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    "poke_id": 10,
                }
            return fake_json

        mock_get_pokemon.side_effect = side_effect_func
        pokemon_names = ["bulbasaur", "ivysaur", "venusaur", "ditto"]
        pokemons = [
            get_or_create_pokemon(pokemon_data=get_pokemon_info(pokemon_name=pokemon_name))
            for pokemon_name in pokemon_names
        ]
        creator_pkns = pokemons[0:3]
        opponent_pkns = pokemons[1:]

        self.add_pokemons_to_team(
            pokemons=creator_pkns, positions=[3, 2, 1], team=self.team_creator
        )
        self.add_pokemons_to_team(
            pokemons=opponent_pkns, positions=[1, 2, 3], team=self.team_opponent
        )
        winner = get_winner(self.battle)
        self.assertTrue(winner)
        self.assertEqual(winner, self.creator)

    def test_opponent_wins_in_a_tie(self):
        self.add_pokemons_to_team(
            pokemons=self.pokemons, positions=[1, 2, 3], team=self.team_creator
        )
        self.add_pokemons_to_team(
            pokemons=self.pokemons, positions=[1, 2, 3], team=self.team_opponent
        )
        winner = get_winner(self.battle)
        self.assertTrue(winner)
        self.assertEqual(winner, self.opponent)

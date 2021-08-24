from model_bakery import baker

from battles.models import TeamPokemon
from battles.services.api_integration import get_pokemon_info
from battles.services.logic_battle import get_winner
from battles.services.logic_team_pokemon import (
    check_pokemons_unique,
    check_position_unique,
    check_team_sum_valid,
)
from common.utils.tests import TestCaseUtils


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

    def test_team_sum_valid(self):
        pokemon_names = ["pikachu", "eevee", "nidorina"]
        pokemons_data = [get_pokemon_info(pokemon_name) for pokemon_name in pokemon_names]
        is_team_sum_valid = check_team_sum_valid(pokemons_data)
        self.assertTrue(is_team_sum_valid)

    def test_team_sum_invalid(self):
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

    def test_get_winner(self):
        print(self.pokemons)
        add_pokemons_to_team(pokemons=self.pokemons, positions=[1, 2, 3], team=self.team_creator)
        add_pokemons_to_team(pokemons=self.pokemons, positions=[3, 2, 1], team=self.team_opponent)
        winner = get_winner(self.battle)
        self.assertTrue(winner)

    def test_opponent_wins_in_a_tie(self):
        add_pokemons_to_team(pokemons=self.pokemons, positions=[1, 2, 3], team=self.team_creator)
        add_pokemons_to_team(pokemons=self.pokemons, positions=[1, 2, 3], team=self.team_opponent)
        winner = get_winner(self.battle)
        self.assertTrue(winner)
        self.assertEqual(winner, self.opponent)


def add_pokemons_to_team(pokemons, positions, team):
    for pokemon, position in zip(pokemons, positions):
        TeamPokemon.objects.create(team=team, pokemon=pokemon, order=position)

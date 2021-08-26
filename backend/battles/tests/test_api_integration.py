from unittest import mock

from battles.services.api_integration import check_pokemons_exists, get_pokemons_data
from battles.services.logic_team_pokemon import check_team_sum_valid
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

        pokemons_data = get_pokemons_data(pokemon_names)

        is_team_sum_valid = check_team_sum_valid(pokemons_data)

        self.assertTrue(is_team_sum_valid)

    @mock.patch("battles.services.api_integration.get_pokemon_api")
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

    @mock.patch("battles.services.api_integration.get_pokemon_api")
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

        is_pokemons_valid = check_pokemons_exists(pokemon_names)

        self.assertTrue(is_pokemons_valid)

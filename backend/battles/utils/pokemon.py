from urllib.parse import urljoin

from django.conf import settings

import requests


def get_pokemon(poke_name):
    url = urljoin(settings.POKE_API_URL, poke_name)
    response = requests.get(url)
    data = response.json()
    pokemon = {
        "name": data["name"],
        "img_url": data["sprites"]["front_default"],
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
    }
    return pokemon


def sum_points(pokemons):
    points = 0
    for pokemon in pokemons:
        points += pokemon["attack"] + pokemon["defense"] + pokemon["hp"]
    return points


def check_valid_team(round_battle, trainer):
    pokemons_id = [getattr(round_battle, trainer + "_pokemon_" + str(i)) for i in range(1, 4)]
    pokemons = [get_pokemon(pokemon) for pokemon in pokemons_id]

    is_valid = sum_points(pokemons) <= 600
    return is_valid

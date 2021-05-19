from urllib.parse import urljoin

from django.conf import settings

import requests

from pokemons.models import Pokemon


def get_pokemon_api(poke_id):
    url = urljoin(settings.POKE_API_URL, poke_id)
    response = requests.get(url)
    data = response.json()
    pokemon = {
        "poke_id": poke_id,
        "name": data["name"],
        "img_url": data["sprites"]["front_default"],
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
    }
    save_pokemon(pokemon)


def save_pokemon(pokemon):
    Pokemon.objects.create(
        poke_id=pokemon.poke_id,
        name=pokemon.name,
        img_url=pokemon.img_url,
        defense=pokemon.defense,
        attack=pokemon.attack,
        hp=pokemon.hp,
    )


def get_pokemon(poke_id):
    pokemon = Pokemon.objects.get(poke_id=poke_id)
    if not pokemon:
        get_pokemon_api(poke_id)
        return Pokemon.objects.get(poke_id=poke_id)
    return pokemon


def sum_points(pokemons):
    points = 0
    for pokemon in pokemons:
        points += pokemon["attack"] + pokemon["defense"] + pokemon["hp"]
    return points


def check_valid_team(round_battle):
    pokemons_id = [getattr(round_battle, "pokemon_" + str(i)) for i in range(1, 4)]
    pokemons = [get_pokemon(pokemon) for pokemon in pokemons_id]
    is_valid = sum_points(pokemons) <= 600
    return is_valid

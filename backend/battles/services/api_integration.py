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
    return pokemon


def save_pokemon(pokemon_response):
    return Pokemon.objects.create(
        poke_id=pokemon_response["poke_id"],
        name=pokemon_response["name"],
        img_url=pokemon_response["img_url"],
        defense=pokemon_response["defense"],
        attack=pokemon_response["attack"],
        hp=pokemon_response["hp"],
    )


def get_or_create_pokemon(poke_id):
    pokemon = Pokemon.objects.filter(poke_id=poke_id).first()
    if not pokemon:
        pokemon_response = get_pokemon_api(poke_id)
        return save_pokemon(pokemon_response)
    return pokemon

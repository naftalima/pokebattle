from urllib.parse import urljoin

from django.conf import settings

import requests

from pokemons.models import Pokemon  # pylint:disable=import-error


def get_pokemon_api(pokemon_name):
    url = urljoin(settings.POKE_API_URL, pokemon_name)
    response = requests.get(url)
    data = response.json()
    pokemon = {
        "poke_id": data["id"],
        "name": pokemon_name,
        "img_url": data["sprites"]["front_default"],
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
    }
    return pokemon


def save_pokemon(pokemon_data):
    return Pokemon.objects.create(
        poke_id=pokemon_data["poke_id"],
        name=pokemon_data["name"],
        img_url=pokemon_data["img_url"],
        defense=pokemon_data["defense"],
        attack=pokemon_data["attack"],
        hp=pokemon_data["hp"],
    )


def get_pokemon_info(pokemon_name):
    pokemon = Pokemon.objects.filter(name=pokemon_name).first()
    if not pokemon:
        pokemon_response = get_pokemon_api(pokemon_name)
        return pokemon_response
    return {
        "poke_id": pokemon.poke_id,
        "name": pokemon_name,
        "img_url": pokemon.img_url,
        "defense": pokemon.defense,
        "attack": pokemon.attack,
        "hp": pokemon.hp,
    }


def get_or_create_pokemon(pokemon_data):
    pokemon = Pokemon.objects.filter(poke_id=int(pokemon_data["poke_id"])).first()
    if not pokemon:
        pokemon = save_pokemon(pokemon_data)
        return pokemon
    return pokemon


def get_all_pokemons_api():
    limit = "?limit=899"
    url = settings.POKE_API_URL + limit
    response = requests.get(url)
    pokeapi_named = response.json().get("results")
    for pokemon_result in pokeapi_named:
        pokemon_name = pokemon_result["name"]
        pokemon = get_pokemon_api(pokemon_name)
        get_or_create_pokemon(pokemon)


def check_pokemons_exists(pokemon_names):
    for pokemon_name in pokemon_names:
        response = get_pokemon_api(pokemon_name)
        if not bool(response):
            return False
    return True


def get_pokemons_data(pokemon_names):
    pokemons_data = [get_pokemon_info(pokemon_name) for pokemon_name in pokemon_names]
    return pokemons_data

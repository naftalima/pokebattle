def sum_points(pokemons_data):
    points = 0
    for pokemon in pokemons_data:
        points += pokemon["attack"] + pokemon["defense"] + pokemon["hp"]
    return points


def check_valid_team(pokemons_data):
    is_valid = sum_points(pokemons_data) <= 600
    return is_valid

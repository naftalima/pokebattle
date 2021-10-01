def sum_points(pokemons_data):
    points = 0
    for pokemon in pokemons_data:
        points += pokemon["attack"] + pokemon["defense"] + pokemon["hp"]
    return points


def check_team_sum_valid(pokemons_data):
    is_valid = sum_points(pokemons_data) <= 600
    return is_valid


def check_position_unique(positions):
    for position in positions:
        if positions.count(position) > 1:
            return False
    return True


def check_pokemons_unique(pokemon_names):
    for pokemon_name in pokemon_names:
        if pokemon_names.count(pokemon_name) > 1:
            return False
    return True

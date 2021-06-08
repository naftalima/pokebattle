def sum_points(pokemons):
    points = 0
    for pokemon in pokemons:
        points += pokemon.attack + pokemon.defense + pokemon.hp
    print(points)
    return points


def check_valid_team(pokemons):
    is_valid = sum_points(pokemons) <= 600
    return is_valid

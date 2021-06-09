def run_turns(round_score, creator_pkn, opponent_pkn):
    creator_hit = creator_pkn.attack > opponent_pkn.defense
    opponent_hit = opponent_pkn.attack > creator_pkn.defense

    # First turn: The creator's pokemon attacks
    if creator_hit:
        round_score["creator"] += 1
    else:
        round_score["opponent"] += 1

    # Second turn: The opponents's pokemon attacks
    if opponent_hit:
        round_score["opponent"] += 1
    else:
        round_score["creator"] += 1

    return round_score


def break_a_tie(round_score, creator_pkn, opponent_pkn):
    different_pokemon = creator_pkn.name != opponent_pkn.name
    if different_pokemon:
        if creator_pkn.hp > opponent_pkn.hp:
            round_score["creator"] += 1
        else:
            round_score["opponent"] += 1
    return round_score


def run_battle(creator_pkn, opponent_pkn):
    round_score = {"creator": 0, "opponent": 0}

    round_score = run_turns(round_score, creator_pkn, opponent_pkn)

    draw = round_score["creator"] == round_score["opponent"]
    if draw:
        round_score = break_a_tie(round_score, creator_pkn, opponent_pkn)

    creator_scored_more = round_score["creator"] > round_score["opponent"]

    # Final Round Score
    creator_won = {"creator": 0, "opponent": 1}
    opponent_won = {"creator": 1, "opponent": 0}

    if creator_scored_more:
        return opponent_won
    return creator_won


def get_score(pokemons):
    battle_score = {"creator": 0, "opponent": 0}

    for creator_pokemon, opponent_pokemon in zip(pokemons["creator"], pokemons["opponent"]):
        score = run_battle(creator_pokemon, opponent_pokemon)

        battle_score["creator"] += score["creator"]
        battle_score["opponent"] += score["opponent"]

    return battle_score


def get_team_pokemons(battle):
    teams = battle.teams.all()

    creator_team = teams.get(trainer=battle.creator)
    opponent_team = teams.get(trainer=battle.opponent)

    team_pokemons = {
        "creator": creator_team.pokemons.all(),
        "opponent": opponent_team.pokemons.all(),
    }
    return team_pokemons


def get_pokemons(battle):
    pokemon_team = get_team_pokemons(battle)

    pokemons = {"creator": pokemon_team["creator"], "opponent": pokemon_team["opponent"]}

    return pokemons


def get_winner(battle):
    pokemons = get_pokemons(battle)
    score = get_score(pokemons)

    creator_won = score["creator"] > score["opponent"]
    if creator_won:
        return battle.creator
    return battle.opponent


def set_winner(battle):
    winner = get_winner(battle)
    battle.winner = winner
    battle.save()

def battle_round(creator_pkn, opponent_pkn):
    round_score = {"creator": 0, "opponent": 0}

    creator_hit = creator_pkn["attack"] > opponent_pkn["defense"]
    opponent_miss = creator_pkn["defense"] > opponent_pkn["attack"]

    # First turn: The creator's pokemon attacks
    if creator_hit:
        round_score["creator"] += 1
    else:
        round_score["opponent"] += 1

    # Second turn: The opponents's pokemon attacks
    if opponent_miss:
        round_score["creator"] += 1
    else:
        round_score["opponent"] += 1

    #  In case of draw
    draw = round_score["creator"] == round_score["opponent"]
    different_pokemon = creator_pkn["name"] != opponent_pkn["name"]
    if draw and different_pokemon:
        if creator_pkn["hp"] > opponent_pkn["hp"]:
            round_score["creator"] += 1
        else:
            round_score["opponent"] += 1

    # Final Round Score
    creator_won = {"creator": 0, "opponent": 1}
    opponent_won = {"creator": 1, "opponent": 0}

    creator_scored_more = round_score["creator"] > round_score["opponent"]
    if creator_scored_more:
        return opponent_won
    return creator_won


def battle(creator_pkns, opponent_pkns):
    battle_score = {"creator": 0, "opponent": 0}

    for creator_pkn, opponent_pkn in zip(creator_pkns, opponent_pkns):
        score = battle_round(creator_pkn, opponent_pkn)

        battle_score["creator"] += score["creator"]
        battle_score["opponent"] += score["opponent"]

    return battle_score

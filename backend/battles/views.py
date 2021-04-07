from urllib.parse import urljoin

from django.conf import settings
from django.shortcuts import redirect, render

import requests

from users.models import User

from .forms import CreatorRoundForm, OpponentRoundForm, TrainersRoundForm
from .models import Battle
from .utils.battle import battle


def get_pokemon(poke_name):
    url = urljoin(settings.POKE_API_URL, poke_name)
    response = requests.get(url)
    data = response.json()
    info = {
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
        "name": data["name"],
    }
    return info


def sum_points(pokemon):
    result = pokemon["attack"] + pokemon["defense"] + pokemon["hp"]
    return result


def check_valid_creator_team(curr_form):
    pokemon1 = get_pokemon(curr_form.creator_pokemon_1)
    pokemon2 = get_pokemon(curr_form.creator_pokemon_2)
    pokemon3 = get_pokemon(curr_form.creator_pokemon_3)
    pokemon1_points = sum_points(pokemon1)
    pokemon2_points = sum_points(pokemon2)
    pokemon3_points = sum_points(pokemon3)
    sum_pokemons_points = pokemon1_points + pokemon2_points + pokemon3_points
    if sum_pokemons_points <= 600:
        return True
    return False


def check_valid_opponent_team(curr_form):
    pokemon1 = get_pokemon(curr_form.opponent_pokemon_1)
    pokemon2 = get_pokemon(curr_form.opponent_pokemon_2)
    pokemon3 = get_pokemon(curr_form.opponent_pokemon_3)
    pokemon1_points = sum_points(pokemon1)
    pokemon2_points = sum_points(pokemon2)
    pokemon3_points = sum_points(pokemon3)
    sum_pokemons_points = pokemon1_points + pokemon2_points + pokemon3_points
    if sum_pokemons_points <= 600:
        return True
    return False


# Create your views here.
def home(request):
    player = User.objects.all()
    return render(request, "battles/home.html", {"player": player})


def invite(request):
    return render(request, "battles/invite.html")


def opponent(request):
    return render(request, "battles/opponent.html")


def select_trainers(request):
    if request.method == "POST":
        print('request.method== "POST"')
        form = TrainersRoundForm(request.POST)
        if form.is_valid():
            form.save(commit=False).save()
            return redirect("creator_pokemons")
    else:
        form = TrainersRoundForm()
    return render(request, "battles/select_trainers.html", {"form": form})


def select_creator_pokemons(request):
    battle_info = Battle.objects.latest("id")
    print(battle_info)
    if request.method == "POST":
        form = CreatorRoundForm(request.POST, instance=battle_info)
        if form.is_valid():
            round_battle = form.save(commit=False)
            valid_team = check_valid_creator_team(round_battle)
            if valid_team:
                form.save(commit=False).save()
                return redirect("invite")
            message = "ERROR: you selected sum more than 600 points"
            return render(request, "battles/create_battle.html", {"form": form, "message": message})
    else:
        form = CreatorRoundForm()
    return render(request, "battles/create_battle.html", {"form": form})


def select_opponent_pokemons(request):
    battle_info = Battle.objects.latest("id")
    if request.method == "POST":
        form = OpponentRoundForm(request.POST, instance=battle_info)
        if form.is_valid():
            round_battle = form.save(commit=False)
            valid_team = check_valid_opponent_team(round_battle)
            if valid_team:
                form.save()
                return redirect("battles")
            message = "ERROR: you selected sum more than 600 points"
            return render(
                request,
                "battles/opponent_pokemons.html",
                {"form": form, "battle": battle_info, "message": message},
            )
    else:
        form = OpponentRoundForm()
    return render(request, "battles/opponent_pokemons.html", {"form": form})


def battles(request):
    battle_id = Battle.objects.latest("id").id
    battle_info = Battle.objects.filter(id=battle_id).values()[0]

    creator_pkms = [get_pokemon(battle_info["creator_pokemon_" + str(i)]) for i in range(1, 4)]
    opponent_pkms = [get_pokemon(battle_info["opponent_pokemon_" + str(i)]) for i in range(1, 4)]

    score = battle(creator_pkms, opponent_pkms)

    winner = "Player1" if score["creator"] > score["opponent"] else "Player2"

    return render(
        request,
        "battles/battle_info.html",
        {
            "winner": winner,
            "creator_pkms": creator_pkms,
            "score": score,
            "opponent_pkms": opponent_pkms,
        },
    )

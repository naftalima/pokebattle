from django.shortcuts import render
from django.shortcuts import redirect
from urllib.parse import urljoin
import requests
from users.models import User
from .models import Battle
from .forms import CreatorRoundForm, OpponentRoundForm
from django.conf import settings

def get_pokemon(poke_name):
    url = urljoin(settings.POKE_API_URL, poke_name)
    response = requests.get(url)
    data = response.json()
    info = {
        "defense": data["stats"][3]["base_stat"],
        "attack": data["stats"][4]["base_stat"],
        "hp": data["stats"][5]["base_stat"],
        "name": data["name"]
    }
    return info

def sum_points(pokemon):
    sumResult = pokemon["attack"] +  pokemon["defense"] + pokemon["hp"]
    return sumResult

def check_valid_creator_team(curr_form):
    pokemon1 = get_pokemon(curr_form.creator_pokemon_1)
    pokemon2 = get_pokemon(curr_form.creator_pokemon_2)
    pokemon3 = get_pokemon(curr_form.creator_pokemon_3)
    pokemon1_points = sum_points(pokemon1)
    pokemon2_points = sum_points(pokemon2)
    pokemon3_points = sum_points(pokemon3)
    sum_pokemons_points = pokemon1_points + pokemon2_points + pokemon3_points
    if sum_pokemons_points <= 600: return True
    else: return False

def check_valid_opponent_team(curr_form):
    pokemon1 = get_pokemon(curr_form.opponent_pokemon_1)
    pokemon2 = get_pokemon(curr_form.opponent_pokemon_2)
    pokemon3 = get_pokemon(curr_form.opponent_pokemon_3)
    pokemon1_points = sum_points(pokemon1)
    pokemon2_points = sum_points(pokemon2)
    pokemon3_points = sum_points(pokemon3)
    sum_pokemons_points = pokemon1_points + pokemon2_points + pokemon3_points
    if sum_pokemons_points <= 600: return True
    else: return False

# Create your views here.
def home(request):
    player = User.objects.all()
    return render(request, 'battles/home.html', { 'player': player })

def invite(request):
    return render(request, 'battles/invite.html')

def opponent(request):
    return render(request, 'battles/opponent.html')

def select_creator_pokemons(request):
    if request.method == "POST":
        print('request.method == "POST"')
        form = CreatorRoundForm(request.POST)
        if form.is_valid():
            round_battle = form.save(commit=False)
            valid_team = check_valid_creator_team(round_battle)
            if valid_team:
                form.save(commit=False).save()
                return redirect('invite')
            else:
                message = "ERROR: you selected sum more than 600 points"
                return render(request, 'battles/create_battle.html', {'form': form,
                                                                      'message': message })
    else:
        form = CreatorRoundForm()
    return render(request, 'battles/create_battle.html', {'form': form})

def select_opponent_pokemons(request):
    battle_info = Battle.objects.latest('id')
    if request.method == "POST":
        form = OpponentRoundForm(request.POST, instance=battle_info)
        if form.is_valid():
            round_battle = form.save(commit=False)
            valid_team = check_valid_opponent_team(round_battle)
            if valid_team:
                form.save()
                return redirect('battle')
            else:
                message = "ERROR: you selected sum more than 600 points"
                return render(request, 'battles/opponent_pokemons.html', {'formRound2': form,
                                                                           'battle': battle_info,
                                                                           'message': message })
    else:
        form = OpponentRoundForm()
    return render(request, 'battles/opponent_pokemons.html', {'formRound2': form})

def battle_round(creator_pkn, opponent_pkn):
    round_score = {'creator': 0, 'opponent': 0}

    creator_hit = creator_pkn['attack'] > opponent_pkn['defense']
    opponent_miss = creator_pkn['defense'] > opponent_pkn['attack']

    # First turn: The creator's pokemon attacks
    if creator_hit:
        round_score['creator'] +=1
    else:
        round_score['opponent'] +=1

    # Second turn: The opponents's pokemon attacks
    if opponent_miss:
        round_score['creator'] +=1
    else:
        round_score['opponent'] +=1

    #  In case of draw
    draw = round_score['creator'] == round_score['opponent']
    different_pokemon = creator_pkn['name'] != opponent_pkn['name']
    if draw and different_pokemon:
        if  creator_pkn['hp'] > opponent_pkn['hp']:
            round_score['creator'] +=1
        else:
            round_score['opponent'] +=1

    # Final Round Score
    creator_won = {'creator': 0, 'opponent': 1}
    opponent_won =  {'creator': 1, 'opponent': 0}

    creator_scored_more = round_score['creator'] > round_score['opponent']
    if creator_scored_more:
        return opponent_won
    return creator_won

def battle(creator_pkns,opponent_pkns):
    battle_score =  {'creator': 0, 'opponent': 0}

    for creator_pkn, opponent_pkn in zip(creator_pkns, opponent_pkns):
        score = battle_round(creator_pkn, opponent_pkn)

        battle_score['creator'] += score['creator']
        battle_score['opponent'] += score['opponent']

    return battle_score

def battles(request):
    battle_id =  Battle.objects.latest('id').id
    battle_info = Battle.objects.filter(id=battle_id).values()[0]

    creator_pokemons = [get_pokemon(battle_info['creator_pokemon_'+ str(i)]) for i in range(1, 4)]
    opponent_pokemons = [get_pokemon(battle_info['opponent_pokemon_'+ str(i)]) for i in range(1, 4)]

    score = battle(creator_pokemons,opponent_pokemons )

    winner = 'Player1' if score['creator'] > score['opponent'] else 'Player2'

    return render(request, 'battles/battle_info.html', {'winner': winner,
                                                        'creator_pokemons': creator_pokemons,
                                                        'score': score,
                                                        'opponent_pokemons': opponent_pokemons })

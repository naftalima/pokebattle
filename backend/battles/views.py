from django.shortcuts import render
from django.shortcuts import redirect
from users.models import User
from .models import Battle
from .forms import CreatorRoundForm, OpponentRoundForm
from urllib.parse import urljoin
from django.conf import settings
import requests

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
    return render(request, 'battles/home.html', { 'player' : player})

def invite(request):
    return render(request, 'battles/invite.html')

def opponent(request):
    return render(request, 'battles/opponent.html')

def creator_pokemons(request):
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
                message = "ERROR: The PKNs you selected sum more than 600 points, please choose again"
                return render(request, 'battles/round.html', {'form': form, 'message':message})
    else:
        form = CreatorRoundForm()
    return render(request, 'battles/round.html', {'form': form})

def opponent_pokemons(request):
    battle_info = Battle.objects.get(id=32)
    if request.method == "POST":
        form = OpponentRoundForm(request.POST, instance=battle_info)
        if form.is_valid():
            round_battle = form.save(commit=False)
            valid_team = check_valid_opponent_team(round_battle)
            if valid_team:
                form.save()
                return redirect('home')
            else:
                message = "ERROR: The PKNs you selected sum more than 600 points, please choose again"
                return render(request, 'battles/round_new2.html', {'formRound2': form, 'battle':battle_info, 'message': message})
    else:
        form = OpponentRoundForm()
    return render(request, 'battles/round_new2.html', {'formRound2': form})

def round (player1_pokemon, player2_pokemon):
    # PKN1 vs PKN2
    # A1 vs D2
    # A2 vs D1
    # HP1 vs HP2 <- settles in case of draw

    round_score = {'player_1': 0, 'player_2': 0}

    if player1_pokemon['attack'] > player2_pokemon['defense']: round_score['player_1'] +=1
    else: round_score['player_2'] +=1
    if player1_pokemon['defense'] > player2_pokemon['attack']: round_score['player_1'] +=1
    else: round_score['player_2'] +=1

    if round_score['player_1'] == round_score['player_2'] and player1_pokemon['hp'] != player2_pokemon['hp']:
        if  player1_pokemon['hp'] > player2_pokemon['hp']: round_score['player_1'] +=1
        else: round_score['player_2'] +=1
    else:
        if round_score['player_1'] > round_score['player_2']: return {'player_1': 1, 'player_2': 0}
        else: return {'player_1': 0, 'player_2': 1}

def battle(battle_info, score):
    for i in range(1,4):
        curr_pkm_c = 'creator_pokemon_' + str(i)
        curr_pkm_o = 'opponent_pokemon_' + str(i)
        creator_pokemon = get_pokemon(battle_info[curr_pkm_c])
        opponent_pokemon = get_pokemon(battle_info[curr_pkm_o])

        roud_score = round(creator_pokemon, opponent_pokemon)
        score['player_1'] += roud_score['player_1']
        score['player_2'] += roud_score['player_2']
    return score

def battles(request):
    battle_info = Battle.objects.filter(id=32).values()[0]
    creator_pokemons = [get_pokemon(battle_info['creator_pokemon_'+ str(i)]) for i in range(1,4) ]
    opponent_pokemons = [get_pokemon(battle_info['opponent_pokemon_'+ str(i)]) for i in range(1,4) ]

    score = {'player_1': 0, 'player_2': 0}
    score = battle(battle_info,score )

    winner = 'Player1' if score['player_1'] > score['player_2'] else 'Player2'

    return render(request, 'battles/battle.html', {'winner':winner,'creator_pokemons':creator_pokemons,'score':score,'opponent_pokemons':opponent_pokemons} )

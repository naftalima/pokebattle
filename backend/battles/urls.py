from django.urls import path

from .views import (
    BattleInfoView,
    HomeView,
    InviteView,
    Opponent,
    SelectCreatorPokemonsView,
    SelectOpponentPokemonsView,
    SelectTrainersView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("battle/", BattleInfoView.as_view(), name="battle_result"),
    path("creator/pokemons", SelectCreatorPokemonsView.as_view(), name="creator_pokemons"),
    path("invite/", InviteView.as_view(), name="invite"),
    path("opponent/", Opponent.as_view(), name="opponent"),
    path("opponent/pokemons", SelectOpponentPokemonsView.as_view(), name="opponent_pokemons"),
    path("trainers", SelectTrainersView.as_view(), name="select_trainers"),
]

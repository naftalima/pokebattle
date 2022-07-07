from django.urls import path

from battles.api.views import (
    BattleDetailView,
    BattleListView,
    CreateBattleView,
    PokemonListView,
    SelectTeamView,
)


urlpatterns = [
    path("battle/new/", CreateBattleView.as_view(), name="battle_create"),
    path("team/<int:pk>/edit/", SelectTeamView.as_view(), name="team_edit"),
    path("battle/", BattleListView.as_view(), name="battle_list"),
    path("pokemon/", PokemonListView.as_view(), name="pokemon_list"),
    path("battle/<int:pk>", BattleDetailView.as_view(), name="battle_detail"),
]

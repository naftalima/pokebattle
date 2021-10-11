from django.urls import path

from battles.views import (
    BaseView,
    BattleDetailView,
    BattleListView,
    CreateBattleView,
    HomeView,
    SelectTeamView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("v2/battle/<int:pk>", BaseView.as_view(), name="v2_battle_detail"),
    path("v2/battle/", BaseView.as_view(), name="v2_battle_list"),
    path("battle/", BattleListView.as_view(), name="battles"),
    path("battle/<int:pk>/", BattleDetailView.as_view(), name="battle-detail"),
    path("battle/new/", CreateBattleView.as_view(), name="battle-opponent"),
    path("battle/<int:pk>/team/new/", SelectTeamView.as_view(), name="battle-team-pokemons"),
]

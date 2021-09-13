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
    path("base", BaseView.as_view(), name="base_react"),
    path("battle/", BattleListView.as_view(), name="battles"),
    path("battle/<int:pk>/", BattleDetailView.as_view(), name="battle-detail"),
    path("battle/new/", CreateBattleView.as_view(), name="battle-opponent"),
    path("battle/<int:pk>/team/new/", SelectTeamView.as_view(), name="battle-team-pokemons"),
]

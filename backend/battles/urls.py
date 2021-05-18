from django.urls import path

from .views import (
    BattleDetailView,
    BattlesView,
    CreateBattleView,
    HomeView,
    LoginView,
    SelectTeamView,
)


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("", HomeView.as_view(), name="home"),
    path("battle/", BattlesView.as_view(), name="battles"),
    path("battle/<int:pk>", BattleDetailView.as_view(), name="battle-detail"),
    path("battle/new/", CreateBattleView.as_view(), name="select_opponent"),
    path("battle/<int:pk>/team/new", SelectTeamView.as_view(), name="select_pokemons"),
]

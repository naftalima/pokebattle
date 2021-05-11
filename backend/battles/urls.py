from django.urls import path

from .views import (
    HomeView,
    LoginView,
    OnGoingBattlesView,
    SelectTeamView,
    SelectTrainersView,
    SettledBattlesView,
)


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("home/", HomeView.as_view(), name="home"),
    path("battle/settled", SettledBattlesView.as_view(), name="settled_battles"),
    path("battle/on_going", OnGoingBattlesView.as_view(), name="on_going_battles"),
    path("battle/new/opponent", SelectTrainersView.as_view(), name="select_opponent"),
    path("battle/new/team", SelectTeamView.as_view(), name="select_pokemons"),
]

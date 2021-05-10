from django.urls import path

from .views import HomeView, LoginView, SelectTeamView, SelectTrainersView


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("home/", HomeView.as_view(), name="home"),
    path("battle/select_opponent", SelectTrainersView.as_view(), name="select_opponent"),
    path("battle/select_team", SelectTeamView.as_view, name="select_pokemons"),
]

from django.urls import path

from .views import BattlesView, HomeView, LoginView, SelectTeamView, SelectTrainersView


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("home/", HomeView.as_view(), name="home"),
    path("battle/", BattlesView.as_view(), name="battles"),
    # TODO: battle information page
    #  path("battle/<int:battle_id>", BattleView.as_view(), name="battle" ),
    path("battle/new/", SelectTrainersView.as_view(), name="select_opponent"),
    path("battle/team/new", SelectTeamView.as_view(), name="select_pokemons")
    # TODO Query Parameters
    # path("battle/<int:battle_id>/team/new", SelectTeamView.as_view(), name="select_pokemons"),
]

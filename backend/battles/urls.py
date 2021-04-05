from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("battle/", views.battles, name="battle"),
    path("create/battle", views.select_creator_pokemons, name="creator_pokemons"),
    path("invite/", views.invite, name="invite"),
    path("opponent/", views.opponent, name="opponent"),
    path("opponent/pokemons", views.select_opponent_pokemons, name="opponent_pokemons"),
]

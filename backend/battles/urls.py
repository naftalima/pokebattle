from django.urls import path

from .views import (
    BattleDetailView,
    BattlesView,
    HomeView,
    LoginView,
    SelectTeamView,
    SelectTrainersView,
)


# TODO Advanced path matching/regular expression primer
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("", HomeView.as_view(), name="home"),
    path("battle/", BattlesView.as_view(), name="battles"),
    # TODO href listview to detailview
    path("battle/<int:pk>", BattleDetailView.as_view(), name="battle-detail"),
    path("battle/new/", SelectTrainersView.as_view(), name="select_opponent"),
    path("battle/team/new", SelectTeamView.as_view(), name="select_pokemons")
    # TODO create team
    # path(r'battle/<int:pk>/team/new', SelectTeamView.as_view(), name='select_pokemons'),
]

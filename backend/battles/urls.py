from django.urls import path

from .views import (
    BattleDetailView,
    BattleListView,
    CreateBattleView,
    HomeView,
    SelectTeamView,
    SignUpView,
    UserLoginView,
)


urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", HomeView.as_view(), name="home"),
    path("battle/", BattleListView.as_view(), name="battles"),
    path("battle/<int:pk>/", BattleDetailView.as_view(), name="battle-detail"),
    path("battle/new/", CreateBattleView.as_view(), name="battle-opponent"),
    path("battle/<int:pk>/team/new/", SelectTeamView.as_view(), name="battle-team-pokemons"),
]

from django.urls import path

from battles.api.views import BattleListView, CreateBattleView, SelectTeamView


urlpatterns = [
    path("battle/", BattleListView.as_view(), name="battle_list"),
    path("battle/new/", CreateBattleView.as_view(), name="battle_create"),
    path("team/<int:pk>/edit/", SelectTeamView.as_view(), name="team_edit"),
]

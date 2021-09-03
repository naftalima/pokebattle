from django.urls import path

from battles.api.views import BattleListView, CreateBattleView


urlpatterns = [
    path("battle/", BattleListView.as_view(), name="battle_list"),
    path("battle/new/", CreateBattleView.as_view(), name="battle_create"),
]

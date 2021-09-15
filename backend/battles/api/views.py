from django.db.models import Q

from rest_framework import generics, permissions

from battles.api.permissions import IsTheTrainerOfTheTeam
from battles.api.serializers import BattleSerializer, CreateBattleSerializer, SelectTeamSerializer
from battles.models import Battle, Team
from battles.services.logic_team import all_teams_has_pokemons
from battles.tasks import run_battle_and_send_result


class BattleListView(generics.ListAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by("-id")
        return queryset


class BattleDetailView(generics.RetrieveAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by("-id")
        return queryset


class CreateBattleView(generics.CreateAPIView):
    serializer_class = CreateBattleSerializer
    permission_classes = [permissions.IsAuthenticated]


class SelectTeamView(generics.UpdateAPIView):
    serializer_class = SelectTeamSerializer
    queryset = Team.objects.all()
    permission_classes = [IsTheTrainerOfTheTeam]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        battle = instance.battle

        teams_are_complete = all_teams_has_pokemons(battle)
        if teams_are_complete:
            run_battle_and_send_result.delay(battle.id)
        return super().update(request, *args, **kwargs)

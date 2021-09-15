from django.db.models import Q

from rest_framework import generics, permissions

from battles.api.permissions import IsTrainerOfTeam
from battles.api.serializers import BattleSerializer, CreateBattleSerializer, SelectTeamSerializer
from battles.models import Battle, Team


class BattleListView(generics.ListAPIView):
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
    permission_classes = [IsTrainerOfTeam]

from django.db.models import Q

from rest_framework import generics

from battles.api.serializers import BattleSerializer, CreateBattleSerializer, SelectTeamSerializer
from battles.models import Battle, Team


class BattleListView(generics.ListAPIView):
    serializer_class = BattleSerializer

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by("-id")
        return queryset


class CreateBattleView(generics.CreateAPIView):
    serializer_class = CreateBattleSerializer


class SelectTeamView(generics.UpdateAPIView):
    serializer_class = SelectTeamSerializer
    queryset = Team.objects.all()

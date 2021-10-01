from django.db.models import Q

from rest_framework import generics, permissions

from battles.api.permissions import IsTrainerOfTeam
from battles.api.serializers import BattleSerializer, CreateBattleSerializer, SelectTeamSerializer
from battles.models import Battle, Team, TeamPokemon
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
    permission_classes = [IsTrainerOfTeam]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        battle = instance.battle

        creator_team_has_pokemons = TeamPokemon.objects.filter(
            team__trainer=battle.creator, team__battle=battle
        ).exists()
        opponent_team_has_pokemons = TeamPokemon.objects.filter(
            team__trainer=battle.opponent, team__battle=battle
        ).exists()
        all_teams_has_pokemons = creator_team_has_pokemons and opponent_team_has_pokemons
        if all_teams_has_pokemons:
            run_battle_and_send_result.delay(battle.id)
        return super().update(request, *args, **kwargs)

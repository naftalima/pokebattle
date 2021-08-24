from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from battles.forms import BattleForm, TeamForm
from battles.models import Battle, Team, TeamPokemon
from battles.services.logic_battle import get_pokemons
from battles.tasks import run_battle_and_send_result
from pokemons.models import Pokemon


class HomeView(TemplateView):
    template_name = "battles/home.html"


class CreateBattleView(LoginRequiredMixin, CreateView):
    model = Battle
    template_name = "battles/battle-opponent.html"
    form_class = BattleForm

    def get_initial(self):
        return {"user_id": self.request.user.id}

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()

        creator_team_id = (
            Team.objects.only("id").get(battle=form.instance, trainer=form.instance.creator).id
        )

        return HttpResponseRedirect(reverse_lazy("battle-team-pokemons", args=(creator_team_id,)))


class SelectTeamView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = "battles/battle-team-pokemons.html"
    form_class = TeamForm

    def form_valid(self, form):
        battle = self.get_object().battle

        form.save()

        creator_team_has_pokemons = TeamPokemon.objects.filter(
            team__trainer=battle.creator, team__battle=battle
        ).exists()
        opponent_team_has_pokemons = TeamPokemon.objects.filter(
            team__trainer=battle.opponent, team__battle=battle
        ).exists()
        all_teams_has_pokemons = creator_team_has_pokemons and opponent_team_has_pokemons
        if all_teams_has_pokemons:
            run_battle_and_send_result.delay(battle.id)
            return HttpResponseRedirect(reverse_lazy("battle-detail", args=(battle.id,)))
        return HttpResponseRedirect(reverse_lazy("battles"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemons_name = list(Pokemon.objects.values_list("name", flat=True))
        context["pokemons_name"] = pokemons_name
        return context


class BattleListView(LoginRequiredMixin, ListView):
    model = Battle
    template_name = "battles/battles.html"
    context_object_name = "battles"

    def get_queryset(self):
        queryset_filtered = Battle.objects.filter(
            Q(creator__exact=self.request.user) | Q(opponent__exact=self.request.user)
        )

        return queryset_filtered

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        queryset_filtered = self.get_queryset()

        context["on_going"] = queryset_filtered.filter(winner__isnull=True).order_by("-id")
        context["settled"] = queryset_filtered.filter(winner__isnull=False).order_by("-id")

        return context


class BattleDetailView(LoginRequiredMixin, DetailView):
    model = Battle
    template_name = "battles/battle_detail.html"
    context_object_name = "battle"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()

        pokemons = get_pokemons(context["battle"])
        context["creator_pokemons"] = pokemons["creator"]
        context["opponent_pokemons"] = pokemons["opponent"]

        return context

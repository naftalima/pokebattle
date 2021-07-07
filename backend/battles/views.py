from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from battles.forms import BattleForm, TeamForm, UserRegisterForm
from battles.models import Battle, Team, TeamPokemon
from battles.services.email import email_battle_result
from battles.services.logic_battle import get_pokemons, get_winner
from users.models import User


class UserLoginView(LoginView):
    redirect_field_name = "home"
    redirect_authenticated_user = True


class SignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "registration/signup.html"
    success_message = "Your profile was created successfully"
    success_url = reverse_lazy("home")


class HomeView(TemplateView):
    template_name = "battles/home.html"


class CreateBattleView(LoginRequiredMixin, CreateView):
    model = Battle
    template_name = "battles/battle-opponent.html"
    form_class = BattleForm

    def get_initial(self):
        return {"user_id": self.request.user.id}

    def form_valid(self, form):
        # TODO init in form
        form.instance.creator = self.request.user
        battle = form.save()

        team_creator = Team.objects.create(battle=battle, trainer=form.instance.creator)
        Team.objects.create(battle=battle, trainer=form.instance.opponent)

        return HttpResponseRedirect(reverse_lazy("battle-team-pokemons", args=(team_creator.id,)))


class SelectTeamView(UpdateView):
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
            winner = get_winner(battle)
            battle.set_winner(winner)
            email_battle_result(battle)
            return HttpResponseRedirect(reverse_lazy("battle-detail", args=(battle.id,)))
        return HttpResponseRedirect(reverse_lazy("battles"))


class BattleListView(LoginRequiredMixin, ListView):
    model = Battle
    template_name = "battles/battles.html"
    context_object_name = "battles"
    # TODO paginate_by = 10

    def get_queryset(self):
        queryset_filtered = Battle.objects.filter(
            Q(creator__exact=self.request.user) | Q(opponent__exact=self.request.user)
        )

        return queryset_filtered

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        queryset_filtered = self.get_queryset()

        context["on_going"] = queryset_filtered.filter(winner__isnull=True)
        context["settled"] = queryset_filtered.filter(winner__isnull=False)

        return context


# BUG: Crashes if run battle 1
class BattleDetailView(DetailView):
    model = Battle
    template_name = "battles/battle_detail.html"
    context_object_name = "battle"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()

        pokemons = get_pokemons(context["battle"])
        context["creator_pokemons"] = pokemons["creator"]
        context["opponent_pokemons"] = pokemons["opponent"]

        return context

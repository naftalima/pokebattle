from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from .forms import BattleForm, TeamForm
from .models import Battle, Team


class LoginView(TemplateView):
    template_name = "battles/login.html"


class HomeView(TemplateView):
    template_name = "battles/home.html"


class CreateBattleView(CreateView):
    model = Battle
    template_name = "battles/battle-opponent.html"
    form_class = BattleForm
    # success_url = reverse_lazy("battle-team-pokemons")

    def get_initial(self):
        return {"user_id": self.request.user.id}

    def form_valid(self, form):
        # TODO init in form
        form.instance.creator = self.request.user
        battle = form.save()

        team_creator = Team.objects.create(battle=battle, trainer=form.instance.creator)
        Team.objects.create(battle=battle, trainer=form.instance.opponent)

        return HttpResponseRedirect(reverse_lazy("battle-team-pokemons", args=(team_creator.id,)))


# HACK : should be a UpdateView
class SelectTeamView(UpdateView):
    model = Team
    template_name = "battles/battle-team-pokemons.html"
    form_class = TeamForm
    success_url = reverse_lazy("battles")

    # TODO : do the validation on the form
    # TODO : pass error message in context


class BattlesView(ListView):  # pylint: disable=too-many-ancestors
    model = Battle
    template_name = "battles/battles.html"
    context_object_name = "battles"
    # TODO paginate_by = 10

    def get_queryset(self):
        queryset_filtered = Battle.objects.filter(
            Q(creator__exact=self.request.user) | Q(opponent__exact=self.request.user)
        )

        return queryset_filtered

    def get_context_data(self):  # pylint: disable=arguments-differ
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

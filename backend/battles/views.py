from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import BattleForm
from .models import Battle, Team


class LoginView(TemplateView):
    template_name = "battles/login.html"


class HomeView(TemplateView):
    template_name = "battles/home.html"


class CreateBattleView(CreateView):
    model = Battle
    template_name = "battles/battle-opponent.html"
    form_class = BattleForm
    success_url = reverse_lazy("battle-team-pokemons")

    def form_valid(self, form):
        # TODO init in form
        form.instance.creator = self.request.user
        battle = form.save()

        Team.objects.create(battle=battle, trainer=form.instance.creator)
        Team.objects.create(battle=battle, trainer=form.instance.opponent)

        response = super(CreateBattleView, self).form_valid(form)
        return response


# HACK : should be a UpdateView
class SelectTeamView(TemplateView):
    template_name = "battles/battle-team-pokemons.html"

    # TODO : do the validation on the form
    # TODO : pass error message in context


class BattlesView(ListView):  # pylint: disable=too-many-ancestors
    model = Battle
    template_name = "battles/battles.html"
    context_object_name = "battles"
    # TODO paginate_by = 10

    def get_queryset(self):
        queryset_filtered = Battle.objects.filter(
            creator__exact=self.request.user
        ) | Battle.objects.filter(opponent__exact=self.request.user)

        queryset = {
            "on_going": queryset_filtered.filter(winner__isnull=True),
            "settled": queryset_filtered.filter(winner__isnull=False),
        }
        return queryset


# BUG: Crashes if run battle 1
class BattleDetailView(DetailView):
    model = Battle
    template_name = "battles/battle_detail.html"
    context_object_name = "battle"

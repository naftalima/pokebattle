from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import TrainersRoundForm
from .models import Battle


class LoginView(TemplateView):
    template_name = "battles/login.html"


class HomeView(TemplateView):
    template_name = "battles/home.html"


class CreateBattleView(CreateView):
    model = Battle
    template_name = "battles/select_trainers.html"
    form_class = TrainersRoundForm
    success_url = reverse_lazy("select_pokemons")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreateBattleView, self).form_valid(form)

    # IDEA I tried this, but I had to modify the field to not null and created migrations
    # def get_initial(self):
    #     initial  = super(CreateBattleView, self).get_initial()
    #     initial['creator'] = self.request.user.pk
    #     print(initial)
    #     return initial


# HACK : should be a CreateView
class SelectTeamView(TemplateView):
    template_name = "battles/select_pokemons.html"

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
    context_object_name = "Battle"

    # FIXME I can't get just the id in the url
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import TrainersRoundForm  # , TeamRoundForm
from .models import Battle  # , Team


class LoginView(TemplateView):
    template_name = "battles/login.html"


class HomeView(TemplateView):
    template_name = "battles/home.html"

    # def get_context_data(self, **kwargs):


class SelectTrainersView(CreateView):
    model = Battle
    template_name = "battles/select_trainers.html"
    form_class = TrainersRoundForm
    success_url = reverse_lazy("select_pokemons")


# TODO
# class SelectTeamView(CreateView):
class SelectTeamView(TemplateView):
    # model = Team
    template_name = "battles/select_pokemons.html"
    # form_class = TeamRoundForm
    # success_url = reverse_lazy("home")

    # TODO: validation in the form
    # def form_valid(self, request):
    # form = self.form_class(request.POST)
    # round_battle = form.save(commit=False)
    # valid_team = check_valid_creator_team(round_battle)
    # if valid_team:
    # return super().form_valid(form)
    # message = "ERROR: you selected sum more than 600 points"
    # return render(request, self.template_name, {"form": self.form_class, "message": message})


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


class BattleDetailView(DetailView):
    model = Battle
    template_name = "battles/battle_detail.html"
    context_object_name = "Battle"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

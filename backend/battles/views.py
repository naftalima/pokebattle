from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import TrainersRoundForm  # , TeamRoundForm
from .models import Battle  # , Team


# from django.views.generic.detail import DetailView


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


# class SettledBattlesView(ListView):
class BattlesView(TemplateView):
    template_name = "battles/battles.html"


# TODO: battle information page
# class BattleView(DetailView):
# template_name = "battles/battle.html"

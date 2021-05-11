from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import TrainersRoundForm
from .models import Battle


class LoginView(TemplateView):
    template_name = "battles/login.html"


class HomeView(TemplateView):
    template_name = "battles/home.html"


class SelectTrainersView(CreateView):
    model = Battle
    template_name = "battles/select_trainers.html"
    form_class = TrainersRoundForm
    success_url = reverse_lazy("select_pokemons")

    # def form_valid(self, form):
    #     self.object = form.save()
    #     return super().form_valid(form)


# class SelectTeamView(CreateView):
class SelectTeamView(TemplateView):
    # model = Team
    template_name = "battles/select_pokemons.html"
    # form_class = TeamRoundForm
    # success_url = reverse_lazy("home")

    # def get_context_data(self, **kwargs):


# class SettledBattlesView(ListView):
class SettledBattlesView(TemplateView):
    template_name = "battles/settled_battles.html"


# class OnGoingBattlesView(ListView):
class OnGoingBattlesView(TemplateView):
    template_name = "battles/on_going_battles.html"

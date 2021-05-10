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
    success_url = reverse_lazy("invite")


class SelectTeamView(CreateView):
    model = Battle
    template_name = "battles/select_pokemons.html"
    form_class = TrainersRoundForm
    success_url = reverse_lazy("invite")

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView

from .forms import CreatorRoundForm, OpponentRoundForm, TrainersRoundForm
from .models import Battle
from .utils.battle import battle
from .utils.pokemon import check_valid_team, get_pokemon


class HomeView(ListView):  # pylint: disable=too-many-ancestors
    model = Battle
    template_name = "battles/home.html"


class InviteView(TemplateView):
    template_name = "battles/invite.html"


class Opponent(View):
    template_name = "battles/opponent.html"

    def get(self, request):
        return render(request, self.template_name)


class SelectTrainersView(CreateView):
    model = Battle
    template_name = "battles/select_trainers.html"
    form_class = TrainersRoundForm
    success_url = reverse_lazy("creator_pokemons")


class SelectCreatorPokemonsView(View):
    model = Battle
    form_class = CreatorRoundForm
    template_name = "battles/create_battle.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        battle_field = self.model.objects.latest("id")
        form = self.form_class(request.POST, instance=battle_field)
        if form.is_valid():
            round_battle = form.save(commit=False)
            valid_team = check_valid_team(round_battle, "creator")
            if valid_team:
                form.save()
                return redirect("invite")
            message = "ERROR: you selected sum more than 600 points"
            return render(
                request, self.template_name, {"form": self.form_class, "message": message}
            )
        return self.get(request)


class SelectOpponentPokemonsView(View):
    model = Battle
    form_class = OpponentRoundForm
    template_name = "battles/opponent_pokemons.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        battle_field = self.model.objects.latest("id")
        form = self.form_class(request.POST, instance=battle_field)
        if form.is_valid():
            round_battle = form.save(commit=False)
            valid_team = check_valid_team(round_battle, "opponent")
            if valid_team:
                form.save()
                return redirect("battles")
            message = "ERROR: you selected sum more than 600 points"
            return render(
                request, self.template_name, {"form": self.form_class, "message": message}
            )
        return self.get(request)


class BattleInfoView(View):
    model = Battle
    template_name = "battles/battle_info.html"

    def get(self, request):
        battle_id = self.model.objects.latest("id").id
        battle_info = self.model.objects.filter(id=battle_id).values()[0]

        creator_pkms = [get_pokemon(battle_info["creator_pokemon_" + str(i)]) for i in range(1, 4)]
        opponent_pkms = [
            get_pokemon(battle_info["opponent_pokemon_" + str(i)]) for i in range(1, 4)
        ]

        score = battle(creator_pkms, opponent_pkms)

        winner = "Creator" if score["creator"] > score["opponent"] else "Opponent"

        return render(
            request,
            self.template_name,
            {
                "winner": winner,
                "creator_pkms": creator_pkms,
                "score": score,
                "opponent_pkms": opponent_pkms,
            },
        )

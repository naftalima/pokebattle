from django import forms
from django.forms import ModelForm

from battles.models import Battle, Team, TeamPokemon
from battles.services.api_integration import get_or_create_pokemon, get_pokemon_info
from battles.services.logic_team_pokemon import check_valid_team
from users.models import User


class BattleForm(ModelForm):
    class Meta:
        model = Battle
        fields = ("opponent",)

    def __init__(self, *args, **kwargs):
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=self.initial["user_id"])


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = [
            "pokemon_1",
            "position_1",
            "pokemon_2",
            "position_2",
            "pokemon_3",
            "position_3",
        ]

    pokemon_1 = forms.IntegerField(
        label="Pokemon 1",
        required=True,
        min_value=1,
        max_value=898,
    )
    pokemon_2 = forms.IntegerField(
        label="Pokemon 2",
        required=True,
        min_value=1,
        max_value=898,
    )
    pokemon_3 = forms.IntegerField(
        label="Pokemon 3",
        required=True,
        min_value=1,
        max_value=898,
    )

    position_1 = forms.IntegerField(
        label="Position 1",
        required=True,
        min_value=1,
        max_value=3,
    )

    position_2 = forms.IntegerField(
        label="Position 2",
        required=True,
        min_value=1,
        max_value=3,
    )

    position_3 = forms.IntegerField(
        label="Position 3",
        required=True,
        min_value=1,
        max_value=3,
    )

    def clean(self):
        cleaned_data = super().clean()

        matrix_position_pokemon = [
            [cleaned_data["position_1"], cleaned_data["pokemon_1"]],
            [cleaned_data["position_2"], cleaned_data["pokemon_2"]],
            [cleaned_data["position_3"], cleaned_data["pokemon_3"]],
        ]

        matrix_position_pokemon = sorted(matrix_position_pokemon, key=(lambda x: x[0]))

        pokemons_id = [str(x[1]) for x in matrix_position_pokemon]
        pokemons_data = [get_pokemon_info(pokemon_id) for pokemon_id in pokemons_id]

        is_team_valid = check_valid_team(pokemons_data)

        if not is_team_valid:
            raise forms.ValidationError(
                "ERROR: Your pokemons sum more than 600 points." "Please select other pokemons"
            )

        cleaned_data["pokemon_1"] = get_or_create_pokemon(pokemons_data[0])
        cleaned_data["pokemon_2"] = get_or_create_pokemon(pokemons_data[1])
        cleaned_data["pokemon_3"] = get_or_create_pokemon(pokemons_data[2])

        return cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        team = self.instance

        team.pokemons.clear()

        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_1"], order=1)
        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_2"], order=2)
        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_3"], order=3)

        return team

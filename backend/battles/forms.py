from django.forms import ModelChoiceField, ModelForm, ValidationError

from battles.models import Battle, Team, TeamPokemon
from battles.services.logic_team_pokemon import check_valid_team
from pokemons.models import Pokemon


class BattleForm(ModelForm):
    class Meta:
        model = Battle
        fields = ("opponent",)


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = [
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
        ]

    pokemon_1 = ModelChoiceField(
        label="Pokemon 1",
        queryset=Pokemon.objects.all(),
        required=True,
    )
    pokemon_2 = ModelChoiceField(
        label="Pokemon 2",
        queryset=Pokemon.objects.all(),
        required=True,
    )
    pokemon_3 = ModelChoiceField(
        label="Pokemon 3",
        queryset=Pokemon.objects.all(),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()

        pokemons = [self.cleaned_data["pokemon_" + str(i)] for i in range(1, 4)]

        is_team_valid = check_valid_team(pokemons)

        if not is_team_valid:
            raise ValidationError(
                "ERROR: Your pokemons sum more than 600 points." "Please select other pokemons"
            )

        return cleaned_data

    def save(self):  # pylint: disable=arguments-differ
        data = self.cleaned_data
        team = self.instance

        team.pokemons.clear()

        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_1"], order=1)
        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_2"], order=2)
        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_3"], order=3)

        return team

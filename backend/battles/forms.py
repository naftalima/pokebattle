from django import forms

from pokemons.models import Pokemon

from .models import Battle, Team, TeamPokemon


class BattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ("opponent",)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
        ]

    pokemon_1 = forms.ModelChoiceField(
        label="Pokemon 1",
        queryset=Pokemon.objects.all(),
        required=True,
    )
    pokemon_2 = forms.ModelChoiceField(
        label="Pokemon 2",
        queryset=Pokemon.objects.all(),
        required=True,
    )
    pokemon_3 = forms.ModelChoiceField(
        label="Pokemon 3",
        queryset=Pokemon.objects.all(),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self):  # pylint: disable=arguments-differ
        data = self.cleaned_data
        team = self.instance

        team.pokemons.clear()

        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_1"], order=1)
        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_2"], order=2)
        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_3"], order=3)

        return team

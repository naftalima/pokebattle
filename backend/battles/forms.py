from django.contrib.auth.forms import UserCreationForm
from django.forms import IntegerField, ModelForm, ValidationError

from battles.models import Battle, Team, TeamPokemon
from battles.services.api_integration import get_or_create_pokemon, get_pokemon_info
from battles.services.logic_team_pokemon import check_valid_team
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email"]


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
            "pokemon_2",
            "pokemon_3",
        ]

    pokemon_1 = IntegerField(
        label="Pokemon 1",
        required=True,
        min_value=1,
        max_value=898,
    )
    pokemon_2 = IntegerField(
        label="Pokemon 2",
        required=True,
        min_value=1,
        max_value=898,
    )
    pokemon_3 = IntegerField(
        label="Pokemon 3",
        required=True,
        min_value=1,
        max_value=898,
    )

    def clean(self):
        cleaned_data = super().clean()

        pokemon_1 = get_pokemon_info(str(cleaned_data["pokemon_1"]))
        pokemon_2 = get_pokemon_info(str(cleaned_data["pokemon_2"]))
        pokemon_3 = get_pokemon_info(str(cleaned_data["pokemon_3"]))

        pokemons_data = [pokemon_1, pokemon_2, pokemon_3]

        is_team_valid = check_valid_team(pokemons_data)

        if not is_team_valid:
            raise ValidationError(
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

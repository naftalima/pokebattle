from django import forms
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.forms import ModelForm
from django.utils.crypto import get_random_string

from battles.models import Battle, Team, TeamPokemon
from battles.services.api_integration import get_or_create_pokemon, get_pokemon_info
from battles.services.email import email_invite
from battles.services.logic_team_pokemon import check_valid_team, is_unique
from users.models import User


class BattleForm(ModelForm):
    opponent = forms.EmailField()

    class Meta:
        model = Battle
        fields = ("opponent",)

    def __init__(self, *args, **kwargs):
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=self.initial["user_id"])
        self.is_guest = False

    def clean_opponent(self):
        opponent_email = self.cleaned_data["opponent"]
        try:
            opponent = User.objects.get(email=opponent_email)
        except User.DoesNotExist:
            self.is_guest = True
            opponent = User.objects.create(email=opponent_email)
            random_password = get_random_string(length=64)
            opponent.set_password(random_password)
            opponent.save()
        return opponent

    def save(self, commit=True):
        super().save()

        battle = self.instance

        Team.objects.create(battle=battle, trainer=battle.creator)
        Team.objects.create(battle=battle, trainer=battle.opponent)

        if not self.is_guest:
            email_invite(battle)
        else:
            opponent = self.cleaned_data["opponent"]
            invite_form = PasswordResetForm(data={"email": opponent.email})
            invite_form.is_valid()
            invite_form.save(
                self,
                subject_template_name="registration/invite_signup_subject.txt",
                email_template_name="registration/password_reset_email.html",
                from_email=settings.EMAIL_ADDRESS,
                html_email_template_name=None,
                extra_email_context={"HOST": settings.HOST},
            )


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

        positions = [
            cleaned_data["position_1"],
            cleaned_data["position_2"],
            cleaned_data["position_3"],
        ]

        is_positions_valid = is_unique(positions)

        if not is_positions_valid:
            raise forms.ValidationError(
                "ERROR: Has repeated positions." " Please select unique positions."
            )

        pokemons_id = [
            cleaned_data["pokemon_1"],
            cleaned_data["pokemon_2"],
            cleaned_data["pokemon_3"],
        ]
        pokemons_id = [str(x) for x in pokemons_id]

        pokemons_data = [get_pokemon_info(pokemon_id) for pokemon_id in pokemons_id]

        is_team_valid = check_valid_team(pokemons_data)

        if not is_team_valid:
            raise forms.ValidationError(
                "ERROR: Your pokemons sum more than 600 points." " Please select other pokemons."
            )

        cleaned_data["pokemon_1"] = get_or_create_pokemon(pokemons_data[0])
        cleaned_data["pokemon_2"] = get_or_create_pokemon(pokemons_data[1])
        cleaned_data["pokemon_3"] = get_or_create_pokemon(pokemons_data[2])

        return cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        team = self.instance

        team.pokemons.clear()

        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_1"], order=data["position_1"])
        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_2"], order=data["position_2"])
        TeamPokemon.objects.create(team=team, pokemon=data["pokemon_3"], order=data["position_3"])

        return team

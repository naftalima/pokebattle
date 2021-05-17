from django import forms

from .models import Battle  # , Team


class TrainersRoundForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ("opponent",)


# class TeamRoundForm(forms.ModelForm):
#     class Meta:
#         model = Team
#         field = ("pokemons")

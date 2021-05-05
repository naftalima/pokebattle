from django import forms

from .models import Battle


class TrainersRoundForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ("creator", "opponent")

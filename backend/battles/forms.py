from django import forms

from .models import Battle


class BattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ("opponent",)

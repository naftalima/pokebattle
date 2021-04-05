from django import forms


from .models import Battle

class CreatorRoundForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('creator', 'opponent', 'creator_pokemon_1',
                  'creator_pokemon_2', 'creator_pokemon_3')


class OpponentRoundForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = ('opponent_pokemon_1', 'opponent_pokemon_2', 'opponent_pokemon_3')

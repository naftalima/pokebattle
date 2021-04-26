from urllib.parse import urljoin

from django.conf import settings
from django.db import models

import requests

from pokemon.models import Pokemon
from users.models import User


class Battle(models.Model):
    url = urljoin(settings.POKE_API_URL, "?limit=20")
    response = requests.get(url)
    data = response.json()

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battle_as_creator")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battle_as_opponent")

    creator_pokemon_1 = models.CharField(
        max_length=200, verbose_name="creator_pokemon_1", null=True
    )
    creator_pokemon_2 = models.CharField(
        max_length=200, verbose_name="creator_pokemon_2", null=True
    )
    creator_pokemon_3 = models.CharField(
        max_length=200, verbose_name="creator_pokemon_3", null=True
    )

    opponent_pokemon_1 = models.CharField(
        max_length=200, verbose_name="opponent_pokemon_1", null=True
    )
    opponent_pokemon_2 = models.CharField(
        max_length=200, verbose_name="opponent_pokemon_2", null=True
    )
    opponent_pokemon_3 = models.CharField(
        max_length=200, verbose_name="opponent_pokemon_3", null=True
    )

    def publish(self):
        self.save()


class Battles(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battles_as_creator")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battles_as_opponent")
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="won_battles", null=True
    )
    creation_date = models.DateTimeField(auto_now_add=True, null=True)


class BattleTeam(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")
    pokemons = models.ManyToManyField(Pokemon, related_name="teams", through="TeamPokemon")
    battle = models.ForeignKey(Battles, on_delete=models.CASCADE, related_name="teams")


class TeamPokemon(models.Model):
    team = models.ForeignKey(BattleTeam, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="pokemons")
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = [("team", "pokemon")]

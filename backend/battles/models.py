from django.db import models

from pokemons.models import Pokemon
from users.models import User


class Battle(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battles_as_creator")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battles_as_opponent")
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="won_battles", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def set_winner(self, winner):
        self.winner = winner
        self.save()


class Team(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")
    pokemons = models.ManyToManyField(Pokemon, related_name="teams", through="TeamPokemon")
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name="teams")


class TeamPokemon(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="pokemons")
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = [("team", "pokemon")]

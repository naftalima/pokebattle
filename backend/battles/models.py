from django.conf import settings
from django.db import models
from urllib.parse import urljoin
import requests
from users.models import User


class Battle(models.Model):
    url = urljoin(settings.POKE_API_URL, "?limit=20")
    response = requests.get(url)
    data = response.json()

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battles_as_creator")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battles_as_opponent")

    creator_pokemon_1 = models.CharField(max_length=200,
                                         verbose_name='creator_pokemon_1', null=True)
    creator_pokemon_2 = models.CharField(max_length=200,
                                         verbose_name='creator_pokemon_2', null=True)
    creator_pokemon_3 = models.CharField(max_length=200,
                                         verbose_name='creator_pokemon_3', null=True)

    opponent_pokemon_1 = models.CharField(max_length=200,
                                          verbose_name='opponent_pokemon_1', null=True)
    opponent_pokemon_2 = models.CharField(max_length=200,
                                          verbose_name='opponent_pokemon_2', null=True)
    opponent_pokemon_3 = models.CharField(max_length=200,
                                          verbose_name='opponent_pokemon_3', null=True)

    def publish(self):
        self.save()

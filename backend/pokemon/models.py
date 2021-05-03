from django.db import models


# Create your models here.
class Pokemon(models.Model):
    poke_id = models.IntegerField(verbose_name="PokeAPI ID")
    name = models.CharField(max_length=50)
    img_url = models.URLField(max_length=500)
    attack = models.IntegerField()
    defense = models.IntegerField()
    hp = models.IntegerField()

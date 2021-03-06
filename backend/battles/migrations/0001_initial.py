# Generated by Django 2.2.19 on 2021-03-23 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator_pokemon_1', models.CharField(max_length=200, null=True, verbose_name='creator_pokemon_1')),
                ('creator_pokemon_2', models.CharField(max_length=200, null=True, verbose_name='creator_pokemon_2')),
                ('creator_pokemon_3', models.CharField(max_length=200, null=True, verbose_name='creator_pokemon_3')),
                ('opponent_pokemon_1', models.CharField(max_length=200, null=True, verbose_name='opponent_pokemon_1')),
                ('opponent_pokemon_2', models.CharField(max_length=200, null=True, verbose_name='opponent_pokemon_2')),
                ('opponent_pokemon_3', models.CharField(max_length=200, null=True, verbose_name='opponent_pokemon_3')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles_as_creator', to=settings.AUTH_USER_MODEL)),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles_as_opponent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

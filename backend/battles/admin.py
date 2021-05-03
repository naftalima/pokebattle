from django.contrib import admin

from .models import Battle, Team, TeamPokemon


admin.site.register(Battle)
admin.site.register(Team)
admin.site.register(TeamPokemon)

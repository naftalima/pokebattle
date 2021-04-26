from django.contrib import admin

from .models import Battle, Battles, BattleTeam, TeamPokemon


admin.site.register(Battle)
admin.site.register(Battles)
admin.site.register(BattleTeam)
admin.site.register(TeamPokemon)

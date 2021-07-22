from django.contrib import admin

from .models import Battle, Team, TeamPokemon


class PokemonsInline(admin.TabularInline):
    model = TeamPokemon
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    inlines = (PokemonsInline,)


admin.site.register(Team, TeamAdmin)
admin.site.register(Battle)
admin.site.register(TeamPokemon)

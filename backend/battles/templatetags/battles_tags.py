from django import template

from battles.models import Battle, Team


register = template.Library()


@register.simple_tag()
def get_total_battles():
    total_battles = Battle.objects.count()
    return total_battles


@register.filter()
def get_team(battle, user):
    team_id = Team.objects.get(battle=battle, trainer=user).id
    return team_id

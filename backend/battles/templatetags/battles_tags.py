# custom_tags.py
from django import template

from ..models import Battle, Team


register = template.Library()


@register.simple_tag()
def total_battles():
    return Battle.objects.count()


@register.filter()
def get_team(battle, user):
    team_id = Team.objects.get(battle=battle, trainer=user).id
    return team_id

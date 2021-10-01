from django import template

from battles.models import Team


register = template.Library()


@register.simple_tag()
def get_total_battles(user):
    total_battles = Team.objects.filter(trainer=user).count()
    return total_battles


@register.filter()
def get_team(battle, user):
    team_id = Team.objects.get(battle=battle, trainer=user).id
    return team_id

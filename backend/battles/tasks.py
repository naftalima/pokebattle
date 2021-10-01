from celery.utils.log import get_task_logger  # pylint:disable=import-error,no-name-in-module

from battles.models import Battle
from battles.services.api_integration import get_all_pokemons_api
from battles.services.email import email_battle_result
from battles.services.logic_battle import get_winner
from pokebattle.celery import app as celery_app


logger = get_task_logger(__name__)


@celery_app.task
def run_battle_and_send_result(battle_id):
    battle = Battle.objects.get(id=battle_id)
    winner = get_winner(battle)
    battle.set_winner(winner)
    email_battle_result(battle)


@celery_app.task
def get_pokemons_from_api_and_save():
    get_all_pokemons_api()

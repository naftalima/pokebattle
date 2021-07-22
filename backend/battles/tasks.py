from celery.utils.log import get_task_logger

from battles.services.api_integration import get_all_pokemons_api
from pokebattle.celery import app as celery_app


logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def get_pokemons_from_api_and_save():
    get_all_pokemons_api()

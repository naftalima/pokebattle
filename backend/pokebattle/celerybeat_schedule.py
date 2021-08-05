from celery.schedules import crontab  # pylint:disable=import-error,no-name-in-module


CELERYBEAT_SCHEDULE = {
    # Internal tasks
    "clearsessions": {"schedule": crontab(hour=3, minute=0), "task": "users.tasks.clearsessions"},
    "get_pokemons_from_api_and_save": {
        "schedule": crontab(0, 0, day_of_month="4"),
        "task": "battles.tasks.get_pokemons_from_api_and_save",
    },
}

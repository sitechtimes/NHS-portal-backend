# core/scripts/clear_db.py

from django.apps import apps
from django.db import connection, transaction


def run():
    print("Deleting all data from the database...")

    with transaction.atomic():
        models = apps.get_models()

        for model in models:
            model.objects.all().delete()
            print(f"\tCleared: {model.__name__}")

        connection.cursor().execute("DELETE FROM sqlite_sequence;")
        print("Reset auto-increment counters.")

    print("Database cleared.")

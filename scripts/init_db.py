from .utils import run_django_command


def run():
    print("\nInitializing database...")
    migration_commands = [
        "makemigrations users",
        "migrate users",
        "makemigrations profiles",
        "migrate profiles",
        "makemigrations guidance",
        "migrate guidance",
        "makemigrations",
        "migrate",
    ]

    for command in migration_commands:
        run_django_command(command)

    print("Database initialized.")

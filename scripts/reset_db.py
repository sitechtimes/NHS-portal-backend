from .utils import run_django_command


def run():
    sure = input("Are you sure you want to reset the database? (y/n) ").lower()
    if sure == "y":
        script_commands = [
            "runscript purge_db",
            "runscript init_db",
            "runscript migrate_users --script-args=fake",
            "runscript create_superuser",
        ]

        for command in script_commands:
            run_django_command(command)

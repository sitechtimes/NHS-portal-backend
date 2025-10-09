from django.test.runner import DiscoverRunner
from django.core.management import call_command


class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # Create the test DB
        db_config = super().setup_databases(**kwargs)

        call_command("flush", "--no-input")
        call_command("runscript", "migrate_users", "--script-args=fake")
        print("Test data loaded into test DB")

        return db_config

from django.core.management.utils import get_random_secret_key


def run():
    secret_key = get_random_secret_key()
    print(f"Django SECRET_KEY:\n{secret_key}")

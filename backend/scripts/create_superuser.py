from users.models import CustomUserManager
import sys


def create_superuser():
    user_manager = CustomUserManager()
    user = user_manager.create_superuser(email="admin@example.com", password="admin")
    print(f"Superuser created: {user.email}")
    return user


def run():
    create_superuser()

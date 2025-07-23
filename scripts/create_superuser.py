from users.models import CustomUser
import sys


def run():
    print("\nCreating superuser...")
    user = CustomUser.objects.create_superuser(
        email="admin@example.com", password="admin"
    )
    print(f"Superuser created:\nemail: {user.email},\npassword: admin")
    return user

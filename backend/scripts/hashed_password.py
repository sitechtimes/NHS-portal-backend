from django.contrib.auth.hashers import make_password


def run():
    test_passwords = ["password"]

    print("🔐 Hashed Passwords:\n")
    for pwd in test_passwords:
        hashed = make_password(pwd)
        print(f"\nRaw: {pwd}\nHashed: {hashed}\n")

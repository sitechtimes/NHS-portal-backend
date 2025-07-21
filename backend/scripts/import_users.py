import os
import csv
from django.db import transaction
from users.models import CustomUser
from django.contrib.auth.hashers import make_password


def run():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.abspath(os.path.join(base_dir, "./data/students.csv"))

    users_to_create = []
    seen_emails = set()
    skipped = 0

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row.get("Student DOE Email", "").strip().lower()
            first_name = row.get("FirstName", "").strip()
            last_name = row.get("LastName", "").strip()
            official_class = row.get("OfficialClass", "").strip()

            if not email or not first_name or not last_name:
                skipped += 1
                continue

            if email in seen_emails or CustomUser.objects.filter(email=email).exists():
                skipped += 1
                continue

            seen_emails.add(email)
            raw_password = email.split("@")[0]

            user = CustomUser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                official_class=official_class,
                user_type=0,
                password=make_password(raw_password),
            )
            users_to_create.append(user)

    with transaction.atomic():
        CustomUser.objects.bulk_create(users_to_create)

    print(f"✅ Created {len(users_to_create)} users")
    print(f"⏭️ Skipped {skipped} rows")

import os
import csv
from django.db import transaction
from users.models import CustomUser
from profiles.models import (
    ServiceProfile,
    LeadershipProfile,
    PersonalProfile,
    GPARecord,
)
from django.contrib.auth.hashers import make_password
from tqdm import tqdm


def run(*args):
    print("\nStarting user migration...")
    use_fake_passwords = "fake" in args
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.abspath(os.path.join(BASE_DIR, "./data/students.csv"))

    seen_emails = set()
    students_to_create = []
    skipped = 0

    existing_emails = set(CustomUser.objects.values_list("email", flat=True))

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = list(csv.DictReader(csvfile))
        total_rows = len(reader)

        # Use tqdm only if real passwords (for progress bar), else just plain iterator
        rows_iter = (
            tqdm(reader, total=total_rows, desc="Processing users", unit="user")
            if not use_fake_passwords
            else reader
        )
        classes = []
        for row in rows_iter:
            email = row.get("Student DOE Email", "").strip().lower()
            first_name = row.get("FirstName", "").strip()
            last_name = row.get("LastName", "").strip()
            official_class = row.get("OfficialClass", "").strip()

            if (
                not email
                or not first_name
                or not last_name
                or not official_class
                or official_class == ""
            ):
                skipped += 1
                continue

            if email in seen_emails or email in existing_emails:
                skipped += 1
                continue

            seen_emails.add(email)
            raw_password = email.split("@")[0]

            if use_fake_passwords:
                # fixed hashed password for testing, raw is "password"
                hashed_password = "pbkdf2_sha256$1000000$0rTiKuDxTigKJRIAJY8iCE$6o6YXkgdkdzLTFYoICkbKn6HIJwyTLffROKW3Zs5K3Q="
            else:
                hashed_password = make_password(raw_password)

            students_to_create.append(
                CustomUser(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    official_class=official_class,
                    user_type=0,
                    password=hashed_password,
                )
            )
    others_to_create = []
    others_to_create.append(
        CustomUser(
            email="teacher1@gmail.com",
            first_name="Sam",
            last_name="Kipnis",
            user_type=1,
            password=hashed_password,
        )
    )
    others_to_create.append(
        CustomUser(
            email="teacher2@gmail.com",
            first_name="Sam2",
            last_name="Kipnis2",
            user_type=1,
            password=hashed_password,
        )
    )
    others_to_create.append(
        CustomUser(
            email="guidance@gmail.com",
            first_name="Sam",
            last_name="Kipnis",
            user_type=2,
            password=hashed_password,
        )
    )
    service_profiles = [ServiceProfile(user=user) for user in students_to_create]
    leadership_profiles = [LeadershipProfile(user=user) for user in students_to_create]
    personal_profiles = [PersonalProfile(user=user) for user in students_to_create]
    gpa_records = [
        GPARecord(gpa=0, year=year, semester=semester, personal_profile=profile)
        for profile in personal_profiles
        for year in range(
            2000 + int(official_class[:2]) - 3, 2000 + int(official_class[:2]) + 1
        )
        for semester in [1, 2]
    ]

    CustomUser.objects.bulk_create(students_to_create + others_to_create)
    ServiceProfile.objects.bulk_create(service_profiles)
    LeadershipProfile.objects.bulk_create(leadership_profiles)
    PersonalProfile.objects.bulk_create(personal_profiles)
    GPARecord.objects.bulk_create(gpa_records)

    print(f"Migrated {len(students_to_create)} users")
    print(f"Skipped {skipped} rows")
    print(
        f"Password mode: {'Fake (Insecure, do not use for production)' if use_fake_passwords else 'REAL (Secure)'}"
    )

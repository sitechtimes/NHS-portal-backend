from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from profiles.models import (
    ServiceProfile,
    LeadershipProfile,
    PersonalProfile,
    GPARecord,
)


@receiver(post_save, sender=CustomUser)
def create_profiles(sender, instance, created, **kwargs):
    if created:
        ServiceProfile.objects.create(user=instance)
        LeadershipProfile.objects.create(user=instance)
        PersonalProfile.objects.create(user=instance)


@receiver(post_save, sender=PersonalProfile)
def create_personal_profile(sender, instance, created, **kwargs):
    if created:
        gpa_records = [
            GPARecord(gpa=0, year=year, semester=semester, personal_profile=instance)
            for year in range(2023, 2026 + 1)
            for semester in [1, 2]
        ]
        GPARecord.objects.bulk_create(gpa_records)

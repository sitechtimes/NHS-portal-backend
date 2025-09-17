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
    if created and instance.user_type == 0:
        ServiceProfile.objects.create(user=instance)
        LeadershipProfile.objects.create(user=instance)
        PersonalProfile.objects.create(user=instance)


@receiver(post_save, sender=PersonalProfile)
def create_personal_profile(sender, instance, created, **kwargs):
    graduation_year = 2000 + int(instance.user.official_class[:2])
    if created:
        gpa_records = [
            GPARecord(gpa=0, year=year, semester=semester, personal_profile=instance)
            for year in range(graduation_year - 3, graduation_year + 1)
            for semester in [1, 2]
        ]
        GPARecord.objects.bulk_create(gpa_records)

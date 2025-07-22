from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from profiles.models import ServiceProfile, LeadershipProfile, PersonalProfile


@receiver(post_save, sender=CustomUser)
def create_profiles(sender, instance, created, **kwargs):
    if created:
        ServiceProfile.objects.create(user=instance)
        LeadershipProfile.objects.create(user=instance)
        PersonalProfile.objects.create(user=instance)

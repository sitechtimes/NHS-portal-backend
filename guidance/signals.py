from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from .models import BiographicalQuestion, BiographicalQuestionInstance


@receiver(post_save, sender=BiographicalQuestion)
def create_biographical_question_instances(sender, instance, created, **kwargs):
    if created:
        students = CustomUser.objects.filter(user_type="0")
        question_instances = [
            BiographicalQuestionInstance(user=student, question=instance)
            for student in students
        ]
        BiographicalQuestionInstance.objects.bulk_create(question_instances)

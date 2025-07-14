from django.db import models
from users.models import CustomUser


class ServiceProfile(Profile):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recommendation_teacher = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LeadershipProfile(Profile):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    teacher_leadership = models.CharField()
    teacher_character = models.CharField()
    teacher_scholarship = models.CharField()

    def __str__(self):
        return self.name


class Activity(models.Model):
    title = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=100)
    screenshot_link = models.CharField(max_length=255)


class ServiceActivity(Activity):
    service_profile = models.ForeignKey(ServiceProfile, on_delete=models.CASCADE)
    grades = models.JSONField(default=list)
    hours = models.IntegerField()

    def __str__(self):
        return self.title


class LeadershipActivity(Activity):
    Leadership_profile = models.ForeignKey(LeadershipProfile, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.title

from django.db import models
from users.models import CustomUser


class ServiceProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="service_profile"
    )
    recommendation_teacher = models.CharField(null=True, blank=True)
    recommendation_given = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class LeadershipProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="leadership_profile"
    )
    teacher_leadership = models.CharField(null=True, blank=True)
    leadership_recommendation_given = models.BooleanField(default=False)
    teacher_character = models.CharField(null=True, blank=True)
    character_recommendation_given = models.BooleanField(default=False)
    teacher_scholarship = models.CharField(null=True, blank=True)
    scholarship_recommendation_given = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PersonalProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="personal_profile"
    )
    gpa = models.FloatField(null=True)
    character_issues = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Personal Profile"


class ServiceActivity(models.Model):
    title = models.CharField(null=True, blank=True)
    supervisor = models.CharField(null=True, blank=True)
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    service_profile = models.ForeignKey(
        ServiceProfile, on_delete=models.CASCADE, related_name="service_activities"
    )
    grades = models.JSONField(default=list, null=True, blank=True)
    hours = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class LeadershipActivity(models.Model):
    title = models.CharField(null=True, blank=True)
    supervisor = models.CharField(null=True, blank=True)
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    leadership_profile = models.ForeignKey(
        LeadershipProfile,
        on_delete=models.CASCADE,
        related_name="leadership_activities",
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

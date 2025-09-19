from django.db import models
from users.models import CustomUser
from events.models import ServiceEvent


class ServiceProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="service_profile"
    )

    def __str__(self):
        return self.name


class LeadershipProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="leadership_profile"
    )

    def __str__(self):
        return self.name


class PersonalProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="personal_profile"
    )
    character_issues = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

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


class EventActivity(models.Model):
    service_event = models.ForeignKey(
        ServiceEvent, on_delete=models.CASCADE, related_name="event_activities"
    )
    service_profile = models.ForeignKey(
        ServiceProfile, on_delete=models.CASCADE, related_name="event_activities"
    )


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


class GPARecord(models.Model):
    personal_profile = models.ForeignKey(
        PersonalProfile,
        on_delete=models.CASCADE,
        related_name="gpa_records",
    )
    semester = models.IntegerField()
    year = models.IntegerField()
    gpa = models.FloatField()

    def __str__(self):
        return f"{self.year} Semester {self.semester} - {self.gpa}"

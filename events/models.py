from django.db import models
from users.models import CustomUser


class ServiceEvent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_events"
    )
    nfc_id = models.IntegerField()

    def __str__(self):
        return self.name

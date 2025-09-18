from django.db import models
from users.models import CustomUser


class ServiceEvent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    nfc_id = models.UUIDField(unique=True)

    def __str__(self):
        return self.name

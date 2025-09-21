from django.db import models
from django.utils import timezone


class ServiceEvent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    nfc_id = models.UUIDField(unique=True)

    @property
    def is_active(self):
        return self.time_start <= timezone.now() <= self.time_end

    def __str__(self):
        return self.name

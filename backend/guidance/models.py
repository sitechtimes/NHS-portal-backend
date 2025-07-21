from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    recipient_emails = models.JSONField(default=list)
    send_immediately = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

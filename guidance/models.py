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


class BiographicalQuestion(models.Model):
    ANSWER_TYPE_CHOICES = [
        ("text", "text"),
        ("dropdown", "dropdown"),
        ("checkbox", "checkbox"),
        ("number", "number"),
    ]
    question_text = models.TextField()
    answer_type = models.CharField(max_length=20, choices=ANSWER_TYPE_CHOICES)
    options = models.JSONField(
        default=list,
        blank=True,
        null=True,
        help_text="Required if answer_type is 'dropdown' or 'checkbox'",
    )

    def __str__(self):
        return self.question_text


class BiographicalQuestionInstance(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="biographical_question_instances"
    )
    question = models.ForeignKey(BiographicalQuestion, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text}"

from django.contrib import admin
from .models import (
    BiographicalQuestion,
    BiographicalQuestionInstance,
    Recommendation,
    Announcement,
)

admin.site.register(BiographicalQuestion)
admin.site.register(BiographicalQuestionInstance)
admin.site.register(Recommendation)
admin.site.register(Announcement)

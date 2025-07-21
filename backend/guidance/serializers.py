from rest_framework import serializers
from .models import Announcement
from users.models import CustomUser
import json
from rest_framework.response import Response


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            "recipient_emails",
            "title",
            "message",
            "send_immediately",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        if not validated_data.get("recipient_emails"):
            recipient_emails = list(
                CustomUser.objects.filter(user_type="0").values_list("email", flat=True)
            )
        else:
            recipient_emails = validated_data.get("recipient_emails")
        print(recipient_emails)
        announcement = Announcement.objects.create(
            title=validated_data["title"],
            message=validated_data["message"],
            recipient_emails=recipient_emails,
            send_immediately=validated_data.get("send_immediately", True),
        )

        if validated_data.get("send_immediately"):
            try:
                from utils.email import send_announcement_email

                send_announcement_email(
                    announcement=announcement, recipient_emails=recipient_emails
                )

                return announcement
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=500,
                )
        return announcement

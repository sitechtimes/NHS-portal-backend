from requests import delete
from rest_framework import serializers
from .models import Announcement, BiographicalQuestion, BiographicalQuestionInstance
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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop("recipient_emails", None)
        rep.pop("send_immediately", None)

        return rep

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


class BiographicalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiographicalQuestion
        fields = ["question_text", "answer_type", "options"]

    def create(self, validated_data):
        if validated_data.get("answer_type") in ["dropdown", "checkbox"]:
            question = BiographicalQuestion.objects.create(
                question_text=validated_data["question_text"],
                answer_type=validated_data["answer_type"],
                options=json.dumps(validated_data["options"]),
            )
        else:
            question = BiographicalQuestion.objects.create(
                question_text=validated_data["question_text"],
                answer_type=validated_data["answer_type"],
            )
        return question


class BiographicalQuestionInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiographicalQuestionInstance
        fields = ["user", "question", "answer"]

    def update(self, instance, validated_data):
        instance.answer = validated_data.get("answer")
        instance.save()
        return instance

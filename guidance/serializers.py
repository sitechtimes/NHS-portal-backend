from rest_framework import serializers
from .models import (
    Announcement,
    BiographicalQuestion,
    BiographicalQuestionInstance,
    Recommendation,
)
from profiles.models import (
    ServiceProfile,
    LeadershipProfile,
    PersonalProfile,
)
from users.models import CustomUser
import json
from rest_framework.response import Response
from django.db.models import Q
from users.serializers import UserSerializer
from profiles.serializers import (
    ServiceProfileSerializer,
    LeadershipProfileSerializer,
    PersonalProfileSerializer,
)


class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = [
            "id",
            "recipient_emails",
            "title",
            "message",
            "created_at",
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

    def delete(self, validated_data):
        announcement = Announcement.objects.get(id=validated_data.get("pk"))
        if announcement.exists():
            announcement.delete()
        return validated_data


class BiographicalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiographicalQuestion
        fields = ["id", "question_text", "answer_type", "options"]

    def create(self, validated_data):
        if validated_data.get("answer_type") not in ["dropdown", "text", "number"]:
            raise serializers.ValidationError("Invalid answer type.")
        if validated_data.get("answer_type") == "dropdown":
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
        students = CustomUser.objects.filter(user_type="0")
        biographical_question_instances = [
            BiographicalQuestionInstance(
                user=student,
                question=question,
            )
            for student in students
        ]
        BiographicalQuestionInstance.objects.bulk_create(
            biographical_question_instances
        )

        return question

    def update(self, instance, validated_data):
        instance.question_text = validated_data.get("question_text")
        instance.answer_type = validated_data.get("answer_type")
        if validated_data.get("answer_type") == "dropdown":
            instance.options = validated_data.get("options")
        instance.save()
        return instance

    def delete(self, validated_data):
        question = BiographicalQuestion.objects.get(id=validated_data.get("pk"))
        if question.exists():
            question.delete()
        return validated_data


class BiographicalQuestionInstanceSerializer(serializers.ModelSerializer):
    question = BiographicalQuestionSerializer()

    class Meta:
        model = BiographicalQuestionInstance
        fields = ["id", "user", "question", "answer"]

    def update(self, instance, validated_data):
        if instance.question.answer_type == "dropdown":
            if validated_data.get("answer") not in json.loads(
                instance.question.options
            ):
                raise serializers.ValidationError("Answer not in options.")
        elif instance.question.answer_type == "number":
            try:
                float(validated_data.get("answer"))
            except ValueError:
                raise serializers.ValidationError("Answer must be a number.")
        elif instance.question.answer_type == "text":
            if not isinstance(validated_data.get("answer"), str):
                raise serializers.ValidationError("Answer must be text.")

        instance.answer = validated_data.get("answer")
        instance.save()
        return instance


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = [
            "id",
            "recommendation_type",
            "teacher_email",
            "submitted_at",
            "approved",
        ]
        read_only_fields = ["id", "submitted_at", "approved"]

    def create(self, validated_data):
        request = self.context.get("request")
        recommendation = Recommendation.objects.create(
            user=request.user,
            recommendation_type=validated_data["recommendation_type"],
            teacher_email=validated_data["teacher_email"],
        )
        return recommendation


class ExpandedRecommendationSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = [
            "id",
            "recommendation_type",
            "teacher_email",
            "submitted_at",
            "approved",
            "student",
        ]

    def get_student(self, obj):
        return UserSerializer(obj.user).data


class ExpandedUserSerializer(serializers.ModelSerializer):
    service_profile = ServiceProfileSerializer()
    leadership_profile = LeadershipProfileSerializer()
    personal_profile = PersonalProfileSerializer()
    biographical_question_instances = BiographicalQuestionInstanceSerializer(many=True)
    recommendations = RecommendationSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "official_class",
            "email",
            "user_type",
            "service_profile",
            "leadership_profile",
            "personal_profile",
            "biographical_question_instances",
            "recommendations",
        ]


class TeacherSerializer(serializers.ModelSerializer):
    recommendation_requests_exist = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "recommendation_requests_exist",
        ]

    def get_recommendation_requests_exist(self, obj):
        return Recommendation.objects.filter(
            Q(teacher_email=obj.email) & (Q(approved=False) | Q(approved__isnull=True))
        ).exists()


class GuidanceSerializer(serializers.ModelSerializer):
    submitted_profiles_exist = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "submitted_profiles_exist",
        ]

    def get_submitted_profiles_exist(self, obj):
        return (
            ServiceProfile.objects.filter(submitted=True).exists()
            | LeadershipProfile.objects.filter(submitted=True).exists()
            | PersonalProfile.objects.filter(submitted=True).exists()
        )

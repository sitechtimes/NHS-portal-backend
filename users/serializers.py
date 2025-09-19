from rest_framework import serializers
from users.models import CustomUser
from profiles.serializers import (
    ExpandedServiceProfileSerializer,
    ExpandedLeadershipProfileSerializer,
    PersonalProfileSerializer,
)
from guidance.serializers import (
    BiographicalQuestionInstanceSerializer,
    RecommendationSerializer,
)
from django.db.models import Sum
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from django.db.models.functions import Coalesce


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "official_class",
            "email",
            "user_type",
            "password",
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            user_type=validated_data["user_type"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            official_class=validated_data["official_class"],
        )
        return user

    def delete(self, validated_data):
        user = CustomUser.objects.filter(id=validated_data.get("pk"))
        if user.exists():
            user.delete()
        return validated_data

    def get(self, instance):
        lookup_field = "email"
        user = CustomUser.objects.get(id=instance.get("pk"))
        return user


class ExpandedUserSerializer(serializers.ModelSerializer):
    service_profile = ExpandedServiceProfileSerializer()
    leadership_profile = ExpandedLeadershipProfileSerializer()
    personal_profile = PersonalProfileSerializer()
    biographical_question_instances = BiographicalQuestionInstanceSerializer(many=True)
    total_hours = serializers.SerializerMethodField()
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
            "total_hours",
            "recommendations",
        ]

    def get_total_hours(self, obj):
        service_profile = obj.service_profile
        service_activity_hours = service_profile.service_activities.aggregate(
            total_hours=Coalesce(Sum("hours"), 0)
        ).get("total_hours", 0)

        event_activity_durations = (
            service_profile.event_activities.annotate(
                duration=ExpressionWrapper(
                    F("service_event__time_end") - F("service_event__time_start"),
                    output_field=DurationField(),
                )
            )
            .aggregate(total_duration=Coalesce(Sum("duration"), None))
            .get("total_duration")
        )

        event_activity_hours = 0
        if event_activity_durations:
            event_activity_hours = event_activity_durations.total_seconds() / 3600

        return service_activity_hours + event_activity_hours

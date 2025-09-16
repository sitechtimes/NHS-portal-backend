from rest_framework import permissions, viewsets, serializers
from users.models import CustomUser
from profiles.serializers import (
    ExpandedServiceProfileSerializer,
    ExpandedLeadershipProfileSerializer,
    PersonalProfileSerializer,
)
from guidance.models import BiographicalQuestionInstance
from guidance.serializers import BiographicalQuestionInstanceSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "official_class",
            "graduation_year",
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
            graduation_year=validated_data.get("graduation_year", None),
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

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "official_class",
            "email",
            "graduation_year",
            "user_type",
            "service_profile",
            "leadership_profile",
            "personal_profile",
            "biographical_question_instances",
            "total_hours",
        ]

    def get_total_hours(self, obj):
        service_profile = obj.service_profile

        total_hours = 0
        for activity in service_profile.service_activities.all():
            print(activity)
            total_hours += activity.hours
        for event_activity in service_profile.event_activities.all():
            print(event_activity)
            event = event_activity.event
            try:
                delta = event.time_end - event.time_start
                total += delta.total_seconds() / 3600.0
            except Exception:
                continue
        return total_hours

from rest_framework import serializers
from events.serializers import EventSerializer
from profiles.models import (
    ServiceProfile,
    LeadershipProfile,
    PersonalProfile,
    ServiceActivity,
    LeadershipActivity,
    GPARecord,
    EventActivity,
)
from users.models import CustomUser
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from django.db.models.functions import Coalesce


# Activity/Event Serializers
class ServiceActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceActivity
        fields = ["id", "title", "supervisor", "grades", "hours", "image"]
        read_only_fields = ["service_profile"]

    def create(self, validated_data):
        user = self.context["request"].user
        service_profile = ServiceProfile.objects.get(user=user)
        if service_profile.submitted:
            raise serializers.ValidationError(
                "Cannot create activity under submitted service profile."
            )
        activity = ServiceActivity.objects.create(
            title=validated_data["title"],
            supervisor=validated_data["supervisor"],
            grades=validated_data["grades"],
            hours=validated_data["hours"],
            image=validated_data["image"],
            service_profile=service_profile,
        )
        return activity

    def delete(self, validated_data):
        activity = ServiceActivity.objects.filter(id=validated_data.get("pk"))
        if activity.service_profile.submitted:
            raise serializers.ValidationError(
                "Cannot delete activity under submitted service profile."
            )
        if activity.exists():
            activity.delete()
        return validated_data

    def update(self, instance, validated_data):
        if instance.service_profile.submitted:
            raise serializers.ValidationError(
                "Cannot update activity under submitted service profile."
            )
        instance.title = validated_data.get("title")
        instance.supervisor = validated_data.get("supervisor")
        instance.grades = validated_data.get("grades")
        instance.hours = validated_data.get("hours")
        instance.image = validated_data.get("image")
        instance.save()
        return instance


class LeadershipActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipActivity
        fields = ["id", "title", "supervisor", "description", "image"]
        read_only_fields = ["leadership_profile"]

    def create(self, validated_data):
        user = self.context["request"].user
        leadership_profile = LeadershipProfile.objects.get(user=user)
        if leadership_profile.submitted:
            raise serializers.ValidationError(
                "Cannot create activity under submitted leadership profile."
            )
        activity = LeadershipActivity.objects.create(
            title=validated_data["title"],
            supervisor=validated_data["supervisor"],
            description=validated_data["description"],
            image=validated_data["image"],
            leadership_profile=leadership_profile,
        )
        return activity

    def delete(self, validated_data):
        activity = LeadershipActivity.objects.filter(id=validated_data.get("pk"))
        if activity.leadership_profile.submitted:
            raise serializers.ValidationError(
                "Cannot delete activity under submitted leadership profile."
            )
        if activity.exists():
            activity.delete()
        return validated_data

    def update(self, instance, validated_data):
        if instance.leadership_profile.submitted:
            raise serializers.ValidationError(
                "Cannot update activity under submitted leadership profile."
            )
        instance.title = validated_data.get("title")
        instance.supervisor = validated_data.get("supervisor")
        instance.description = validated_data.get("description")
        instance.image = validated_data.get("image")
        instance.save()
        return instance


class EventActivitySerializer(serializers.ModelSerializer):
    service_event = EventSerializer()

    class Meta:
        model = EventActivity
        fields = [
            "id",
            "service_event",
        ]


# GPA Serializer
class GPARecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPARecord
        fields = ["id", "gpa", "semester", "year"]

    def update(self, instance, validated_data):
        if instance.personal_profile.submitted:
            raise serializers.ValidationError(
                "Cannot update gpa under submitted personal profile."
            )
        instance.gpa = validated_data.get("gpa")
        instance.save()
        return instance


# Profile Serializers
class ServiceProfileSerializer(serializers.ModelSerializer):
    service_activities = ServiceActivitySerializer(many=True)
    event_activities = EventActivitySerializer(many=True)
    total_hours = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProfile
        fields = [
            "id",
            "service_activities",
            "event_activities",
            "total_hours",
            "submitted",
        ]
        read_only_fields = ["id", "submitted"]

    def get_total_hours(self, obj):
        service_activity_hours = obj.service_activities.aggregate(
            total_hours=Coalesce(Sum("hours"), 0)
        ).get("total_hours", 0)

        event_activity_durations = (
            obj.event_activities.annotate(
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


class LeadershipProfileSerializer(serializers.ModelSerializer):
    leadership_activities = LeadershipActivitySerializer(many=True)

    class Meta:
        model = LeadershipProfile
        fields = [
            "id",
            "leadership_activities",
            "submitted",
        ]
        read_only_fields = ["id", "submitted"]


class PersonalProfileSerializer(serializers.ModelSerializer):
    gpa_records = GPARecordSerializer(many=True, read_only=True)

    class Meta:
        model = PersonalProfile
        fields = ["id", "gpa_records", "character_issues", "notes", "submitted"]
        read_only_fields = ["id", "submitted"]

    def update(self, instance, validated_data):
        if instance.submitted:
            raise serializers.ValidationError(
                "Cannot update submitted personal profile."
            )
        instance.character_issues = validated_data.get("character_issues")
        instance.notes = validated_data.get("notes")
        instance.save()
        return instance

import email
import os
from rest_framework import permissions, viewsets, serializers
from events.serializers import EventSerializer
from profiles.models import (
    ServiceProfile,
    LeadershipProfile,
    PersonalProfile,
    ServiceActivity,
    ServiceEvent,
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
        if activity.exists():
            activity.delete()
        return validated_data

    def update(self, instance, validated_data):
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
        if activity.exists():
            activity.delete()
        return validated_data

    def update(self, instance, validated_data):
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

    def create(self, validated_data):
        user = self.context["request"].user
        personal_profile = PersonalProfile.objects.get(user=user)
        gpa_record = GPARecord.objects.create(
            personal_profile=personal_profile,
            gpa=validated_data["gpa"],
            year=validated_data["year"],
            semester=validated_data["semester"],
        )
        return gpa_record

    def update(self, instance, validated_data):
        instance.gpa = validated_data.get("gpa")
        instance.save()
        return instance


# Profile Serializers
class ServiceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProfile
        fields = ["id"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = CustomUser.objects.get(id=validated_data["user_id"])
        profile = ServiceProfile.objects.create(
            user=user,
        )
        return profile

    def delete(self, validated_data):
        profile = ServiceProfile.objects.get(id=validated_data.get("pk"))
        if profile.exists():
            profile.delete()
        return validated_data

    def update(self, instance, validated_data):
        instance.recommendation_teacher = validated_data.get("recommendation_teacher")
        instance.save()
        return instance


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
        ]
        read_only_fields = ["user"]

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
    class Meta:
        model = LeadershipProfile
        fields = [
            "id",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = CustomUser.objects.get(id=validated_data["user_id"])
        profile = LeadershipProfile.objects.create(
            user=user,
        )
        return profile

    def delete(self, validated_data):
        profile = LeadershipProfile.objects.get(id=validated_data.get("pk"))
        if profile.exists():
            profile.delete()
        return validated_data


class LeadershipProfileSerializer(serializers.ModelSerializer):
    leadership_activities = LeadershipActivitySerializer(many=True)

    class Meta:
        model = LeadershipProfile
        fields = [
            "id",
            "leadership_activities",
        ]
        read_only_fields = ["id"]


class PersonalProfileSerializer(serializers.ModelSerializer):
    gpa_records = GPARecordSerializer(many=True, read_only=True)

    class Meta:
        model = PersonalProfile
        fields = ["id", "gpa_records", "character_issues", "notes"]

    def update(self, instance, validated_data):
        instance.character_issues = validated_data.get("character_issues")
        instance.notes = validated_data.get("notes")
        instance.save()
        return instance

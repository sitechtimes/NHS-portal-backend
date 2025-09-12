import email
from rest_framework import permissions, viewsets, serializers
from profiles.models import (
    ServiceProfile,
    LeadershipProfile,
    PersonalProfile,
    ServiceActivity,
    LeadershipActivity,
    GPARecord,
    EventParticipation,
)
from users.models import CustomUser


class ServiceActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceActivity
        fields = ["title", "supervisor", "grades", "hours", "image"]
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
        # service_profile = ServiceProfile.objects.get(id=validated_data.get("pk"))
        instance.title = validated_data.get("title")
        instance.supervisor = validated_data.get("supervisor")
        instance.grades = validated_data.get("grades")
        instance.hours = validated_data.get("hours")
        instance.image = validated_data.get("image")
        instance.save()
        return instance


class EventParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipation
        fields = ["service_event", "service_profile"]

    def create(self, validated_data):
        student = CustomUser.objects.get(email=validated_data["email"])
        service_profile = ServiceProfile.objects.get(user=student)
        participation = EventParticipation.objects.create(
            service_event=validated_data["service_event"],
            service_profile=service_profile,
        )
        return participation


class LeadershipActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipActivity
        fields = ["title", "supervisor", "description", "image"]
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


class ServiceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProfile
        fields = ["id", "recommendation_teacher"]
        read_only_fields = ["recommendation_given", "user"]

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


class ExpandedServiceProfileSerializer(serializers.ModelSerializer):
    service_activities = ServiceActivitySerializer(many=True)
    event_participations = EventParticipationSerializer(many=True)

    class Meta:
        model = ServiceProfile
        fields = [
            "id",
            "recommendation_teacher",
            "recommendation_given",
            "service_activities",
            "event_participations",
        ]
        read_only_fields = ["user"]


class LeadershipProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipProfile
        fields = [
            "id",
            "teacher_leadership",
            "teacher_character",
            "teacher_scholarship",
        ]
        read_only_fields = [
            "leadership_recommendation_given",
            "character_recommendation_given",
            "scholarship_recommendation_given",
            "user",
        ]

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

    def update(self, instance, validated_data):
        instance.teacher_leadership = validated_data.get("teacher_leadership")
        instance.teacher_character = validated_data.get("teacher_character")
        instance.teacher_scholarship = validated_data.get("teacher_scholarship")
        instance.save()
        return instance


class ExpandedLeadershipProfileSerializer(serializers.ModelSerializer):
    leadership_activities = LeadershipActivitySerializer(many=True)

    class Meta:
        model = LeadershipProfile
        fields = [
            "id",
            "teacher_leadership",
            "leadership_recommendation_given",
            "teacher_character",
            "character_recommendation_given",
            "teacher_scholarship",
            "scholarship_recommendation_given",
            "leadership_activities",
        ]
        read_only_fields = ["user"]


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


class PersonalProfileSerializer(serializers.ModelSerializer):
    gpa_records = GPARecordSerializer(many=True, read_only=True)

    class Meta:
        model = PersonalProfile
        fields = ["id", "gpa_records", "character_issues"]
        read_only_fields = ["user"]

    def update(self, instance, validated_data):
        instance.character_issues = validated_data.get("character_issues")
        instance.save()
        return instance

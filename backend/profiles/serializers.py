from rest_framework import permissions, viewsets, serializers
from profiles.models import (
    ServiceProfile,
    LeadershipProfile,
    ServiceActivity,
    LeadershipActivity,
)


class ServiceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProfile
        fields = [
            "first_name",
            "last_name",
            "osis_last_four_digits",
            "official_class",
            "email",
        ]

    def create(self, validated_data):
        profile = ServiceProfile.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            osis_last_four_digits=validated_data["osis_last_four_digits"],
            official_class=validated_data["official_class"],
            email=validated_data["email"],
        )
        return profile

    def delete(self, validated_data):
        profile = ServiceProfile.objects.filter(id=validated_data.get("pk"))
        if profile.exists():
            profile.delete()
        return validated_data


class LeadershipProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipProfile
        fields = [
            "first_name",
            "last_name",
            "osis_last_four_digits",
            "official_class",
            "email",
            "teacher_leadership",
            "teacher_character",
            "teacher_scholarship",
        ]

    def create(self, validated_data):
        profile = LeadershipProfile.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            osis_last_four_digits=validated_data["osis_last_four_digits"],
            official_class=validated_data["official_class"],
            email=validated_data["email"],
        )
        return profile

    def delete(self, validated_data):
        profile = LeadershipProfile.objects.filter(id=validated_data.get("pk"))
        if profile.exists():
            profile.delete()
        return validated_data


class ServiceActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceActivity
        fields = [
            "title",
            "supervisor",
            "screenshot_link",
            "service_profile",
            "grades",
            "hours",
        ]

    def create(self, validated_data):
        activity = ServiceActivity.objects.create(
            title=validated_data["title"],
            supervisor=validated_data["supervisor"],
            screenshot_link=validated_data["screenshot_link"],
            service_profile=validated_data["service_profile"],
            grades=validated_data["grades"],
            hours=validated_data["hours"],
        )
        return activity

    def delete(self, validated_data):
        activity = ServiceActivity.objects.filter(id=validated_data.get("pk"))
        if activity.exists():
            activity.delete()
        return validated_data


class LeadershipActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipActivity
        fields = [
            "title",
            "supervisor",
            "screenshot_link",
            "leadership_profile",
            "description",
        ]

    def create(self, validated_data):
        activity = LeadershipActivity.objects.create(
            title=validated_data["title"],
            supervisor=validated_data["supervisor"],
            screenshot_link=validated_data["screenshot_link"],
            leadership_profile=validated_data["leadership_profile"],
            description=validated_data["description"],
        )
        return activity

    def delete(self, validated_data):
        activity = LeadershipActivity.objects.filter(id=validated_data.get("pk"))
        if activity.exists():
            activity.delete()
        return validated_data

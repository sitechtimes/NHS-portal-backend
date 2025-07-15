from rest_framework import permissions, viewsets, serializers
from profiles.models import (
    ServiceProfile,
    LeadershipProfile,
    ServiceActivity,
    LeadershipActivity,
)
from users.models import CustomUser


class ServiceActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceActivity
        fields = [
            "title",
            "supervisor",
            "screenshot_link",
            "grades",
            "hours",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        service_profile = ServiceProfile.objects.get(user=user)
        activity = ServiceActivity.objects.create(
            title=validated_data["title"],
            supervisor=validated_data["supervisor"],
            screenshot_link=validated_data["screenshot_link"],
            grades=validated_data["grades"],
            hours=validated_data["hours"],
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
        instance.screenshot_link = validated_data.get("screenshot_link")
        instance.grades = validated_data.get("grades")
        instance.hours = validated_data.get("hours")
        instance.save()
        return instance


class LeadershipActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipActivity
        fields = [
            "title",
            "supervisor",
            "screenshot_link",
            "description",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        leadership_profile = LeadershipProfile.objects.get(user=user)
        activity = LeadershipActivity.objects.create(
            title=validated_data["title"],
            supervisor=validated_data["supervisor"],
            screenshot_link=validated_data["screenshot_link"],
            description=validated_data["description"],
            leadership_profile=leadership_profile,
        )
        return activity

    def delete(self, validated_data):
        activity = LeadershipActivity.objects.filter(id=validated_data.get("pk"))
        if activity.exists():
            activity.delete()
        return validated_data

    def update(self, instance, validated_data):
        # service_profile = ServiceProfile.objects.get(id=validated_data.get("pk"))
        instance.title = validated_data.get("title")
        instance.supervisor = validated_data.get("supervisor")
        instance.screenshot_link = validated_data.get("screenshot_link")
        instance.description = validated_data.get("description")
        instance.save()
        return instance


class ServiceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProfile
        fields = ["id", "recommendation_teacher"]

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
        # service_profile = ServiceProfile.objects.get(id=validated_data.get("pk"))
        instance.recommendation_teacher = validated_data.get("recommendation_teacher")
        instance.save()
        return instance


class ExpandedServiceProfileSerializer(serializers.ModelSerializer):
    service_activity = ServiceActivitySerializer(many=True, read_only=True)

    class Meta:
        model = ServiceProfile
        fields = ["id", "recommendation_teacher", "service_activity"]


class LeadershipProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipProfile
        fields = [
            "id",
            "teacher_leadership",
            "teacher_character",
            "teacher_scholarship",
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
        # print(validated_data)
        instance.teacher_leadership = validated_data.get("teacher_leadership")
        instance.teacher_character = validated_data.get("teacher_character")
        instance.teacher_scholarship = validated_data.get("teacher_scholarship")
        instance.save()
        return instance


class ExpandedLeadershipProfileSerializer(serializers.ModelSerializer):
    leadership_activity = LeadershipActivitySerializer(many=True, read_only=True)

    class Meta:
        model = LeadershipProfile
        fields = [
            "id",
            "teacher_leadership",
            "teacher_character",
            "teacher_scholarship",
            "leadership_activity",
        ]

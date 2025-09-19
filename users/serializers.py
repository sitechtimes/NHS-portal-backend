from rest_framework import serializers
from users.models import CustomUser
from guidance.models import Recommendation
from profiles.serializers import (
    ServiceProfileSerializer,
    LeadershipProfileSerializer,
    PersonalProfileSerializer,
)
from guidance.serializers import (
    BiographicalQuestionInstanceSerializer,
    RecommendationSerializer,
)
from django.db.models import Q


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
    service_profile = ServiceProfileSerializer()
    leadership_profile = LeadershipProfileSerializer()
    personal_profile = PersonalProfileSerializer()
    biographical_question_instances = BiographicalQuestionInstanceSerializer(many=True)
    recommendations = RecommendationSerializer(many=True)
    recommendation_requests = serializers.SerializerMethodField()

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
            "recommendation_requests",
        ]

    def get_recommendation_requests(self, obj):
        requests = Recommendation.objects.filter(
            Q(teacher_email=obj.email) & (Q(approved=True) | Q(approved__isnull=True))
        )
        return RecommendationSerializer(requests, many=True).data

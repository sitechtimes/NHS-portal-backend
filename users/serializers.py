from rest_framework import permissions, viewsets, serializers
from users.models import CustomUser
from profiles.serializers import (
    ExpandedServiceProfileSerializer,
    ExpandedLeadershipProfileSerializer,
    PersonalProfileSerializer,
)


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
        ]

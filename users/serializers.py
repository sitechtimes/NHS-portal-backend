from rest_framework import serializers
from users.models import CustomUser
from guidance.models import Recommendation
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    service_hours = serializers.SerializerMethodField()

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
            "service_hours",
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

    def get_service_hours(self, obj):
        if hasattr(obj, "service_profile"):
            return obj.service_profile.total_hours
        else:
            return 0

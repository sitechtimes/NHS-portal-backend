from rest_framework import permissions, viewsets, serializers
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "osis_last_four_digits",
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
            osis_last_four_digits=validated_data["osis_last_four_digits"],
            official_class=validated_data["official_class"],
        )
        return user

    def delete(self, validated_data):
        user = CustomUser.objects.filter(id=validated_data.get("pk"))
        if user.exists():
            user.delete()
        return validated_data

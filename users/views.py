from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import AllowAny
from backend.permissions import IsGuidance, IsAdmin
from users.serializers import UserSerializer
from users.models import CustomUser


class CreateUser(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsGuidance | IsAdmin]


# When created, a signal creates the profiles


class DeleteUser(DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsGuidance | IsAdmin]

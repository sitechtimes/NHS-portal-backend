from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from profiles.serializers import (
    ServiceActivitySerializer,
    LeadershipActivitySerializer,
    ServiceProfileSerializer,
    LeadershipProfileSerializer,
)
from profiles.models import (
    ServiceActivity,
    LeadershipActivity,
    ServiceProfile,
    LeadershipProfile,
)


class CreateServiceActivity(CreateAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [AllowAny]


class DeleteServiceActivity(DestroyAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [AllowAny]


class UpdateServiceActivity(UpdateAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [AllowAny]


class CreateLeadershipActivity(CreateAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [AllowAny]


class DeleteLeadershipActivity(DestroyAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [AllowAny]


class UpdateLeadershipActivity(UpdateAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [AllowAny]


class UpdateServiceProfile(UpdateAPIView):
    queryset = ServiceProfile.objects.all()
    serializer_class = ServiceProfileSerializer
    permission_classes = [AllowAny]


class UpdateLeadershipProfile(UpdateAPIView):
    queryset = LeadershipProfile.objects.all()
    serializer_class = LeadershipProfileSerializer
    permission_classes = [AllowAny]

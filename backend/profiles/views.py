from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser
from backend.permissions import (
    IsStudent,
    IsOwner,
    OwnsServiceProfileOfActivity,
    OwnsLeadershipProfileOfActivity,
)
from profiles.serializers import (
    ServiceActivitySerializer,
    LeadershipActivitySerializer,
    ServiceProfileSerializer,
    LeadershipProfileSerializer,
    PersonalProfileSerializer,
)
from profiles.models import (
    ServiceActivity,
    LeadershipActivity,
    ServiceProfile,
    LeadershipProfile,
    PersonalProfile,
)


class CreateServiceActivity(CreateAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [IsStudent]


class DeleteServiceActivity(DestroyAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [OwnsServiceProfileOfActivity]


class UpdateServiceActivity(UpdateAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [OwnsServiceProfileOfActivity]


class CreateLeadershipActivity(CreateAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [IsStudent]


class DeleteLeadershipActivity(DestroyAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [OwnsLeadershipProfileOfActivity]


class UpdateLeadershipActivity(UpdateAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [OwnsLeadershipProfileOfActivity]


class UpdateServiceProfile(UpdateAPIView):
    queryset = ServiceProfile.objects.all()
    serializer_class = ServiceProfileSerializer
    permission_classes = [IsOwner]


class UpdateLeadershipProfile(UpdateAPIView):
    queryset = LeadershipProfile.objects.all()
    serializer_class = LeadershipProfileSerializer
    permission_classes = [IsOwner]


class UpdatePersonalProfile(UpdateAPIView):
    queryset = PersonalProfile.objects.all()
    serializer_class = PersonalProfileSerializer
    permission_classes = [IsOwner]

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from backend.permissions import (
    IsStudent,
    IsOwner,
    IsGuidance,
    IsAdmin,
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
    permission_classes = [OwnsServiceProfileOfActivity | IsGuidance | IsAdmin]


class UpdateServiceActivity(UpdateAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [OwnsServiceProfileOfActivity | IsGuidance | IsAdmin]


class CreateLeadershipActivity(CreateAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [IsStudent]


class DeleteLeadershipActivity(DestroyAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [OwnsLeadershipProfileOfActivity | IsGuidance | IsAdmin]


class UpdateLeadershipActivity(UpdateAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [OwnsLeadershipProfileOfActivity | IsGuidance | IsAdmin]


class UpdateServiceProfile(UpdateAPIView):
    queryset = ServiceProfile.objects.all()
    serializer_class = ServiceProfileSerializer
    permission_classes = [IsOwner | IsGuidance | IsAdmin]


class UpdateLeadershipProfile(UpdateAPIView):
    queryset = LeadershipProfile.objects.all()
    serializer_class = LeadershipProfileSerializer
    permission_classes = [IsOwner | IsGuidance | IsAdmin]


class UpdatePersonalProfile(UpdateAPIView):
    queryset = PersonalProfile.objects.all()
    serializer_class = PersonalProfileSerializer
    permission_classes = [IsOwner | IsGuidance | IsAdmin]

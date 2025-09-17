from calendar import c
from sched import Event
import os
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    GenericAPIView,
    RetrieveAPIView,
)
from backend.permissions import (
    IsStudent,
    IsOwner,
    IsGuidance,
    IsAdmin,
    OwnsServiceProfileOfObject,
    OwnsLeadershipProfileOfObject,
    OwnsPersonalProfileOfObject,
)
from profiles.serializers import (
    ServiceActivitySerializer,
    LeadershipActivitySerializer,
    ServiceProfileSerializer,
    LeadershipProfileSerializer,
    PersonalProfileSerializer,
    GPARecordSerializer,
    EventActivitySerializer,
    ExpandedServiceProfileSerializer,
    ExpandedLeadershipProfileSerializer,
)
from profiles.models import (
    ServiceActivity,
    LeadershipActivity,
    ServiceProfile,
    LeadershipProfile,
    PersonalProfile,
    GPARecord,
    EventActivity,
    ServiceEvent,
)
from rest_framework.response import Response


# Service Activity Views
class CreateServiceActivity(CreateAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [IsStudent]


class DeleteServiceActivity(DestroyAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [OwnsServiceProfileOfObject | IsGuidance | IsAdmin]


class UpdateServiceActivity(UpdateAPIView):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    permission_classes = [OwnsServiceProfileOfObject | IsGuidance | IsAdmin]


# Leadership Activity Views
class CreateLeadershipActivity(CreateAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [IsStudent]


class DeleteLeadershipActivity(DestroyAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [OwnsLeadershipProfileOfObject | IsGuidance | IsAdmin]


class UpdateLeadershipActivity(UpdateAPIView):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer
    permission_classes = [OwnsLeadershipProfileOfObject | IsGuidance | IsAdmin]


# Profile Views
class UpdateServiceProfile(UpdateAPIView):
    queryset = ServiceProfile.objects.all()
    serializer_class = ServiceProfileSerializer
    permission_classes = [IsOwner | IsGuidance | IsAdmin]


class RetrieveServiceProfile(RetrieveAPIView):
    queryset = ServiceProfile.objects.all()
    serializer_class = ExpandedServiceProfileSerializer
    permission_classes = [IsOwner | IsGuidance | IsAdmin]


class UpdateLeadershipProfile(UpdateAPIView):
    queryset = LeadershipProfile.objects.all()
    serializer_class = LeadershipProfileSerializer
    permission_classes = [IsOwner | IsGuidance | IsAdmin]


class RetrieveLeadershipProfile(RetrieveAPIView):
    queryset = LeadershipProfile.objects.all()
    serializer_class = ExpandedLeadershipProfileSerializer
    permission_classes = [IsOwner | IsGuidance | IsAdmin]


class UpdatePersonalProfile(UpdateAPIView):
    queryset = PersonalProfile.objects.all()
    serializer_class = PersonalProfileSerializer
    permission_classes = [IsGuidance | IsAdmin]


class RetrievePersonalProfile(RetrieveAPIView):
    queryset = PersonalProfile.objects.all()
    serializer_class = PersonalProfileSerializer
    permission_classes = [IsOwner | IsGuidance | IsAdmin]


# GPA Record Views
class UpdateGPARecord(UpdateAPIView):
    queryset = GPARecord.objects.all()
    serializer_class = GPARecordSerializer
    permission_classes = [OwnsPersonalProfileOfObject | IsGuidance | IsAdmin]


# Event API endpoints
class CreateEventActivity(GenericAPIView):
    queryset = EventActivity.objects.all()
    serializer_class = EventActivitySerializer

    def post(self, request, *args, **kwargs):
        if request.data.get("api_key") != os.getenv("EVENTS_API_KEY"):
            return Response({"error": "Invalid API key"}, status=403)
        service_profile = ServiceProfile.objects.get(
            user__email=request.data.get("email")
        )
        service_event = ServiceEvent.objects.get(nfc_id=request.data.get("nfc_id"))
        event_activity = EventActivity.objects.create(
            service_event=service_event,
            service_profile=service_profile,
        )
        return Response(EventActivitySerializer(event_activity).data)

import os
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from profiles.serializers import (
    ServiceActivitySerializer,
    LeadershipActivitySerializer,
    PersonalProfileSerializer,
    GPARecordSerializer,
    EventActivitySerializer,
    ServiceProfileSerializer,
    LeadershipProfileSerializer,
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
from backend.permissions import (
    IsStudent,
    IsOwner,
    IsGuidance,
    IsAdmin,
    OwnsServiceProfileOfObject,
    OwnsLeadershipProfileOfObject,
    OwnsPersonalProfileOfObject,
)
from rest_framework.decorators import action


class ServiceActivityViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer

    def get_permissions(self):
        if self.action == "create":
            perms = [IsStudent]
        elif self.action in ("partial_update", "destroy"):
            perms = [OwnsServiceProfileOfObject | IsGuidance | IsAdmin]
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]


class LeadershipActivityViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = LeadershipActivity.objects.all()
    serializer_class = LeadershipActivitySerializer

    def get_permissions(self):
        if self.action == "create":
            perms = [IsStudent]
        elif self.action in ("partial_update", "destroy"):
            perms = [OwnsLeadershipProfileOfObject | IsGuidance | IsAdmin]
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]


class ServiceProfileViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ServiceProfile.objects.all()
    serializer_class = ServiceProfileSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "submit"):
            perms = [IsOwner | IsGuidance | IsAdmin]
        elif self.action == "unsubmit":
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        service_profile = self.get_object()
        service_profile.submitted = True
        service_profile.save()
        serializer = ServiceProfileSerializer(service_profile)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def unsubmit(self, request, pk=None):
        service_profile = self.get_object()
        service_profile.submitted = False
        service_profile.save()
        serializer = ServiceProfileSerializer(service_profile)
        return Response(serializer.data)


class LeadershipProfileViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = LeadershipProfile.objects.all()
    serializer_class = LeadershipProfileSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "submit"):
            perms = [IsOwner | IsGuidance | IsAdmin]
        elif self.action == "unsubmit":
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        leadership_profile = self.get_object()
        leadership_profile.submitted = True
        leadership_profile.save()
        serializer = LeadershipProfileSerializer(leadership_profile)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def unsubmit(self, request, pk=None):
        leadership_profile = self.get_object()
        leadership_profile.submitted = False
        leadership_profile.save()
        serializer = LeadershipProfileSerializer(leadership_profile)
        return Response(serializer.data)


class PersonalProfileViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = PersonalProfile.objects.all()
    serializer_class = PersonalProfileSerializer

    def get_permissions(self):
        if self.action == "partial_update":
            perms = [IsGuidance | IsAdmin]
        elif self.action in ("retrieve", "submit"):
            perms = [IsOwner | IsGuidance | IsAdmin]
        elif self.action == "unsubmit":
            perms = [IsGuidance | IsAdmin]
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        personal_profile = self.get_object()
        personal_profile.submitted = True
        personal_profile.save()
        serializer = PersonalProfileSerializer(personal_profile)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def unsubmit(self, request, pk=None):
        personal_profile = self.get_object()
        personal_profile.submitted = False
        personal_profile.save()
        serializer = PersonalProfileSerializer(personal_profile)
        return Response(serializer.data)


class GPARecordViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = GPARecord.objects.all()
    serializer_class = GPARecordSerializer

    def get_permissions(self):
        if self.action == "partial_update":
            perms = [OwnsPersonalProfileOfObject | IsGuidance | IsAdmin]
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]


class EventActivityViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = EventActivity.objects.all()
    serializer_class = EventActivitySerializer

    def get_permissions(self):
        # allow the external service to POST (auth via api_key)
        if self.action == "create":
            return [AllowAny()]

    def create(self, request, *args, **kwargs):
        api_key = request.data.get("api_key")
        if api_key != os.getenv("EVENTS_API_KEY"):
            return Response(
                {"error": "Invalid API key"}, status=status.HTTP_403_FORBIDDEN
            )

        email = request.data.get("email")
        nfc_id = request.data.get("nfc_id")
        if not email or not nfc_id:
            return Response(
                {"error": "Missing 'email' or 'nfc_id' in request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            service_profile = ServiceProfile.objects.get(user__email=email)
        except ServiceProfile.DoesNotExist:
            return Response(
                {"error": "ServiceProfile not found for provided email."}, status=404
            )

        try:
            service_event = ServiceEvent.objects.get(nfc_id=nfc_id)
        except ServiceEvent.DoesNotExist:
            return Response(
                {"error": "ServiceEvent not found for provided nfc_id."}, status=404
            )

        event_activity = EventActivity.objects.create(
            service_event=service_event,
            service_profile=service_profile,
        )
        serializer = self.get_serializer(event_activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

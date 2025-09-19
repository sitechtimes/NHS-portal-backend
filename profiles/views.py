import os
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
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


class ServiceActivityViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ "
    - create: POST /profiles/service_activities/  (create activity)
    - partial_update: PATCH /profiles/service_activities/{pk}/  (partial update)
    - destroy: DELETE /profiles/service_activities/{pk}/  (delete activity)
    """

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
    """
    - create: POST /profiles/leadership_activities/  (create activity)
    - partial_update: PATCH /profiles/leadership_activities/{pk}/  (partial update)
    - destroy: DELETE /profiles/leadership_activities/{pk}/  (delete activity
    """

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
    """
    - retrieve: GET /profiles/service_profiles/{pk}/  (retrieve service profile)
    """

    queryset = ServiceProfile.objects.all()
    serializer_class = ServiceProfileSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            perms = [IsOwner | IsGuidance | IsAdmin]
        return [p() for p in perms]


class LeadershipProfileViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    - retrieve: GET /profiles/leadership_profiles/{pk}/  (retrieve leadership profile)
    """

    queryset = LeadershipProfile.objects.all()
    serializer_class = LeadershipProfileSerializer

    def get_permissions(self):
        perms = [IsOwner | IsGuidance | IsAdmin]
        return [p() for p in perms]


class PersonalProfileViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    - retrieve: GET /profiles/personal_profiles/{pk}/  (retrieve personal profile)
    - partial_update: PATCH /profiles/personal_profiles/{pk}/  (partial update)
    """

    queryset = PersonalProfile.objects.all()
    serializer_class = PersonalProfileSerializer

    def get_permissions(self):
        if self.action == "partial_update":
            perms = [IsGuidance | IsAdmin]
        elif self.action == "retrieve":
            perms = [IsOwner | IsGuidance | IsAdmin]
        return [p() for p in perms]


class GPARecordViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    - partial_update: PATCH /profiles/gpa_records/{pk}/  (partial update)
    """

    queryset = GPARecord.objects.all()
    serializer_class = GPARecordSerializer

    def get_permissions(self):
        if self.action == "partial_update":
            perms = [OwnsPersonalProfileOfObject | IsGuidance | IsAdmin]
        return [p() for p in perms]


class EventActivityViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Endpoint used by NFC backend to post event participation.
    Only exposes create (POST) and validates EVENTS_API_KEY.
    """

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

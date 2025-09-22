import json
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.serializers import UserSerializer
from guidance.serializers import (
    ExpandedUserSerializer,
    TeacherSerializer,
    GuidanceSerializer,
)
from .models import (
    Announcement,
    BiographicalQuestion,
    BiographicalQuestionInstance,
    Recommendation,
)
from profiles.models import ServiceProfile, LeadershipProfile, PersonalProfile
from .serializers import (
    AnnouncementSerializer,
    BiographicalQuestionSerializer,
    BiographicalQuestionInstanceSerializer,
    GuidanceSerializer,
    RecommendationSerializer,
)
from profiles.serializers import (
    ServiceProfileSerializer,
    LeadershipProfileSerializer,
    PersonalProfileSerializer,
)
from backend.permissions import (
    IsTeacher,
    IsGuidance,
    IsAdmin,
    IsSelf,
    OwnsQuestionInstance,
)
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.db.models import Q


class StudentViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = CustomUser.objects.filter(user_type="0")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ("list", "multiple", "filter"):
            perms = [IsGuidance | IsAdmin]
        elif self.action in ("retrieve", "expanded"):
            perms = [IsSelf | IsGuidance | IsAdmin]
        return [p() for p in perms]

    @action(detail=True, methods=["get"])
    def expanded(self, request, pk=None):
        user = self.get_object()
        serializer = ExpandedUserSerializer(user, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def multiple(self, request):
        ids_raw = request.query_params.get("ids")
        try:
            ids = json.loads(ids_raw) if ids_raw else []
        except Exception:
            return Response(
                {"detail": "Invalid ids parameter"}, status=status.HTTP_400_BAD_REQUEST
            )
        users = CustomUser.objects.filter(user_type="0", id__in=ids)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def filter(self, request):
        params = request.query_params
        queryset = CustomUser.objects.filter(user_type="0")
        for param in params:
            if param in ["first_name", "last_name", "official_class", "email"]:
                queryset = queryset.filter(**{f"{param}__icontains": params.get(param)})
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class AnnouncementViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Announcement.objects.all().order_by("-created_at")
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.action in ("create", "destroy"):
            perms = [IsTeacher | IsGuidance | IsAdmin]
        elif self.action == "list":
            perms = [IsAuthenticated]
        return [p() for p in perms]


class BiographicalQuestionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = BiographicalQuestion.objects.all()
    serializer_class = BiographicalQuestionSerializer

    def get_permissions(self):
        if self.action in ("create", "destroy"):
            perms = [IsGuidance | IsAdmin]
        elif self.action == "list":
            perms = [IsAuthenticated]
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]


class BiographicalQuestionInstanceViewSet(
    mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = BiographicalQuestionInstance.objects.all()
    serializer_class = BiographicalQuestionInstanceSerializer

    def get_permissions(self):
        if self.action == "partial_update":
            perms = [OwnsQuestionInstance | IsAdmin]
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    def get_permissions(self):
        if self.action in ("approve", "deny"):
            perms = [IsTeacher | IsGuidance | IsAdmin]
        elif self.action == "create":
            perms = [IsSelf | IsAdmin]
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]

    def create(self, request, *args, **kwargs):
        user = request.user
        recommendation_type = request.data.get("recommendation_type")
        email = request.data.get("teacher_email")
        if not CustomUser.objects.filter(email=email, user_type="1").exists():
            return Response(
                {"error": "No teacher found for provided email."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Recommendation.objects.filter(
            Q(user=user)
            & Q(recommendation_type=recommendation_type)
            & (Q(approved=False) | Q(approved__isnull=True))
        ).exists():
            return Response(
                {
                    "error": "You already have a pending recommendation request of this type."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        rec = self.get_object()
        rec.approved = True
        rec.save()
        return Response(self.get_serializer(rec).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def deny(self, request, pk=None):
        rec = self.get_object()
        rec.approved = False
        rec.save()
        return Response(self.get_serializer(rec).data, status=status.HTTP_200_OK)


class TeacherDashboardView(RetrieveAPIView):
    queryset = CustomUser.objects.filter(user_type="1")
    serializer_class = TeacherSerializer
    permission_classes = [IsSelf]


class TeacherRecommendationRequestsView(ListAPIView):
    serializer_class = RecommendationSerializer

    def get_queryset(self):
        return Recommendation.objects.filter(
            (Q(approved=False) | Q(approved__isnull=True))
            & Q(teacher_email=self.request.user.email)
        )


class GuidanceDashboardView(RetrieveAPIView):
    queryset = CustomUser.objects.filter(user_type="2")
    serializer_class = GuidanceSerializer
    permission_classes = [IsSelf]


class GuidanceSubmittedProfilesView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsGuidance | IsAdmin]

    def get_queryset(self):
        return CustomUser.objects.filter(
            Q(user_type="0")
            & Q(service_profile__submitted=True)
            & Q(leadership_profile__submitted=True)
            & Q(personal_profile__submitted=True)
        )

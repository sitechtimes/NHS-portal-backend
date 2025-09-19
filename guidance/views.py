import json
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.serializers import UserSerializer, ExpandedUserSerializer
from .models import (
    Announcement,
    BiographicalQuestion,
    BiographicalQuestionInstance,
    Recommendation,
)
from .serializers import (
    AnnouncementSerializer,
    BiographicalQuestionSerializer,
    BiographicalQuestionInstanceSerializer,
    RecommendationSerializer,
)
from backend.permissions import (
    IsStudent,
    IsTeacher,
    IsGuidance,
    IsAdmin,
    IsSelf,
    OwnsQuestionInstance,
)


class StudentViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    - retrieve: GET /guidance/users/{pk}/  (student detail)
    - list: GET /guidance/users/           (all students)
    - GET /guidance/users/{pk}/expanded/  (expanded student view)
    - GET /guidance/users/multiple/?ids=[1,2]  (multiple students)
    - GET /guidance/users/filter/?first_name=...  (filter)
    """

    queryset = CustomUser.objects.filter(user_type="0")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "list", "multiple", "filter", "expanded"):
            perms = [IsSelf | IsGuidance | IsAdmin]
        elif self.action == "give_recommendation":
            perms = [IsTeacher | IsAdmin]
        else:
            perms = [IsGuidance | IsAdmin]
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
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    - create: POST /guidance/announcements/  (create announcement)
    - list: GET /guidance/announcements/     (list announcements)
    - destroy: DELETE /guidance/announcements/{pk}/  (delete announcement)
    - submit: POST /guidance/announcements/{pk}/submit/  (submit announcement)
    """

    queryset = Announcement.objects.all().order_by("-created_at")
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.action in ("create", "destroy"):
            perms = [IsTeacher | IsGuidance | IsAdmin]
        else:  # list
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
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]


class BiographicalQuestionInstanceViewSet(
    mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    - update: PATCH /guidance/question-instances/{pk}/     (update question instance)
    """

    queryset = BiographicalQuestionInstance.objects.all()
    serializer_class = BiographicalQuestionInstanceSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update"):
            perms = [OwnsQuestionInstance | IsAdmin]
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all().order_by("-submitted_at")
    serializer_class = RecommendationSerializer

    def get_permissions(self):
        if self.action in ("approve", "deny"):
            perms = [IsTeacher | IsGuidance | IsAdmin]
        elif self.action == "create":
            perms = [IsSelf | IsAdmin]
        else:
            perms = [IsTeacher | IsGuidance | IsAdmin]
        return [p() for p in perms]

    def create(self, request, *args, **kwargs):
        user = request.user
        rtype = request.data.get("recommendation_type")
        if Recommendation.objects.filter(
            user=user, recommendation_type=rtype, approved__in=[True, None]
        ).exists():
            return Response(
                {"detail": "A request of this type is already pending or approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsTeacher | IsGuidance | IsAdmin],
    )
    def approve(self, request, pk=None):
        rec = self.get_object()
        rec.approved = True
        rec.save()
        return Response(self.get_serializer(rec).data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsTeacher | IsGuidance | IsAdmin],
    )
    def deny(self, request, pk=None):
        rec = self.get_object()
        rec.approved = False
        rec.save()
        return Response(self.get_serializer(rec).data, status=status.HTTP_200_OK)

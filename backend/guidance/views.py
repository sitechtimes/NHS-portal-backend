import json
from django.shortcuts import render
from django.core.mail import send_mass_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
    GenericAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from backend.permissions import (
    IsStudent,
    IsTeacher,
    IsGuidance,
    IsAdmin,
    IsSelf,
)
from users.models import CustomUser
from users.serializers import UserSerializer, ExpandedUserSerializer
from .models import Announcement
from .serializers import AnnouncementSerializer


class StudentView(RetrieveAPIView):
    queryset = CustomUser.objects.filter(user_type="0")
    serializer_class = UserSerializer
    permission_classes = [IsSelf | IsTeacher | IsGuidance | IsAdmin]


class ExpandedStudentView(RetrieveAPIView):
    queryset = CustomUser.objects.filter(user_type="0")
    serializer_class = ExpandedUserSerializer
    permission_classes = [IsSelf | IsTeacher | IsGuidance | IsAdmin]


class MultipleStudentsView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsGuidance | IsAdmin]

    def get_queryset(self):
        return CustomUser.objects.filter(
            user_type="0", id__in=json.loads(self.request.query_params.get("ids"))
        )


class FilterStudentsView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsGuidance | IsAdmin]

    def get_queryset(self):
        params = self.request.query_params
        queryset = CustomUser.objects.filter(user_type="0")
        for param in params:
            if param in [
                "first_name",
                "last_name",
                "official_class",
                "email",
                "graduation_year",
            ]:
                queryset = queryset.filter(**{f"{param}__icontains": params.get(param)})

        return queryset


class AllStudentsView(ListAPIView):
    queryset = CustomUser.objects.filter(user_type="0")
    serializer_class = UserSerializer
    permission_classes = [IsGuidance | IsAdmin]


class GiveRecommendation(GenericAPIView):
    permission_classes = [IsTeacher | IsGuidance | IsAdmin]
    serializer_class = ExpandedUserSerializer

    def post(self, request):
        student_id = request.data.get("student_id")
        recommendation_type = request.data.get("recommendation_type")

        student = CustomUser.objects.get(id=student_id, user_type="0")

        if recommendation_type == "service":
            profile = student.service_profile
            profile.recommendation_given = True
        elif recommendation_type in ["leadership", "character", "scholarship"]:
            profile = student.leadership_profile
            if recommendation_type == "leadership":
                profile.leadership_recommendation_given = True
            elif recommendation_type == "character":
                profile.character_recommendation_given = True
            elif recommendation_type == "scholarship":
                profile.scholarship_recommendation_given = True
        profile.save()

        serializer = self.get_serializer(student)
        return Response(serializer.data, status=200)


class CreateAnnouncement(CreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsGuidance | IsAdmin]

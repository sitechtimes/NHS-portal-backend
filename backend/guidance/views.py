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


class StudentView(RetrieveAPIView):
    queryset = CustomUser.objects.filter(user_type="0")
    serializer_class = UserSerializer
    permission_classes = [(IsSelf & IsStudent) | IsTeacher | IsGuidance | IsAdmin]


class ExpandedStudentView(RetrieveAPIView):
    queryset = CustomUser.objects.filter(user_type="0")
    serializer_class = ExpandedUserSerializer
    permission_classes = [(IsSelf & IsStudent) | IsTeacher | IsGuidance | IsAdmin]


class MultipleStudentsView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsTeacher | IsGuidance | IsAdmin]

    def get_queryset(self):
        return CustomUser.objects.filter(
            user_type="0", id__in=json.loads(self.request.query_params.get("ids"))
        )


class FilterStudentsView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsTeacher | IsGuidance | IsAdmin]

    def get_queryset(self):
        params = self.request.query_params
        queryset = CustomUser.objects.filter(user_type="0")
        for param in params:
            if param in [
                "first_name",
                "last_name",
                "osis_last_four_digits",
                "official_class",
                "email",
                "graduation_year",
            ]:
                queryset = queryset.filter(**{f"{param}__icontains": params.get(param)})

        return queryset


class AllStudentsView(ListAPIView):
    queryset = CustomUser.objects.filter(user_type="0")
    serializer_class = UserSerializer
    permission_classes = [IsTeacher | IsGuidance | IsAdmin]

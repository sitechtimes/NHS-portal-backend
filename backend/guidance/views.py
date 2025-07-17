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
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [(IsSelf & IsStudent) | IsTeacher | IsGuidance | IsAdmin]


class ExpandedStudentView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
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
        first_name = params.get("first_name")
        last_name = params.get("last_name")
        osis_last_four_digits = params.get("osis_last_four_digits")
        official_class = params.get("official_class")
        email = params.get("email")
        graduation_year = params.get("graduation_year")

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if osis_last_four_digits:
            queryset = queryset.filter(osis_last_four_digits=osis_last_four_digits)
        if official_class:
            queryset = queryset.filter(official_class=official_class)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if graduation_year:
            queryset = queryset.filter(graduation_year=graduation_year)

        return queryset


class AllStudentsView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsTeacher | IsGuidance | IsAdmin]

    def get_queryset(self):
        return CustomUser.objects.filter(user_type="0")

from django.shortcuts import render
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
from users.models import CustomUser
from users.serializers import UserSerializer, ExpandedUserSerializer


class StudentView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ExpandedStudentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, format=None):
        user = CustomUser.objects.get(id=pk)
        serializer = ExpandedUserSerializer(user)
        return Response(serializer.data)


class AllStudentsView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CustomUser.objects.filter(user_type="0")

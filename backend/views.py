from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
)
from backend.permissions import (
    IsTeacher,
    IsGuidance,
    IsAdmin,
)
from .models import ServiceEvent
from .serializers import EventSerializer


class CreateEventView(CreateAPIView):
    queryset = ServiceEvent.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsTeacher | IsGuidance | IsAdmin]


class StudentEventActivityView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

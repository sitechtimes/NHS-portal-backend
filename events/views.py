from rest_framework import mixins, viewsets
from backend.permissions import IsStudent, IsTeacher, IsGuidance, IsAdmin
from .models import ServiceEvent
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = ServiceEvent.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "list"):
            perms = [IsStudent | IsTeacher | IsGuidance | IsAdmin]
        elif self.action == "create":
            perms = [IsTeacher | IsGuidance | IsAdmin]
        else:
            perms = [IsGuidance | IsAdmin]
        return [p() for p in perms]

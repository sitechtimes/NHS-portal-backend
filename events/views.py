from rest_framework import mixins, viewsets
from backend.permissions import IsTeacher, IsGuidance, IsAdmin
from .models import ServiceEvent
from .serializers import EventSerializer


class EventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    - create: POST /events/  (create event)
    """

    queryset = ServiceEvent.objects.all()
    serializer_class = EventSerializer

    action_permissions = {
        "create": [IsTeacher(), IsGuidance(), IsAdmin()],
    }

    def get_permissions(self):
        return self.action_permissions.get(self.action)

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ServiceActivityViewSet,
    LeadershipActivityViewSet,
    ServiceProfileViewSet,
    LeadershipProfileViewSet,
    PersonalProfileViewSet,
    GPARecordViewSet,
    EventActivityViewSet,
)

router = DefaultRouter()
router.register(
    r"service-activities", ServiceActivityViewSet, basename="service-activity"
)
router.register(
    r"leadership-activities", LeadershipActivityViewSet, basename="leadership-activity"
)
router.register(r"service-profiles", ServiceProfileViewSet, basename="service-profile")
router.register(
    r"leadership-profiles", LeadershipProfileViewSet, basename="leadership-profile"
)
router.register(
    r"personal-profiles", PersonalProfileViewSet, basename="personal-profile"
)
router.register(r"gpa-records", GPARecordViewSet, basename="gpa-record")
router.register(r"event-activities", EventActivityViewSet, basename="event-activity")

urlpatterns = [
    path("", include(router.urls)),
]

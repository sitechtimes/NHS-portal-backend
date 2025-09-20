from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    StudentViewSet,
    AnnouncementViewSet,
    BiographicalQuestionViewSet,
    BiographicalQuestionInstanceViewSet,
    RecommendationViewSet,
    TeacherDashboardView,
)

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="guidance-user")
router.register(r"announcements", AnnouncementViewSet, basename="announcement")
router.register(
    r"questions",
    BiographicalQuestionViewSet,
    basename="question",
)
router.register(
    r"question-instances",
    BiographicalQuestionInstanceViewSet,
    basename="question-instances",
)
router.register(r"recommendations", RecommendationViewSet, basename="recommendation")

urlpatterns = [
    path("", include(router.urls)),
    path("teacher-dashboard/<int:pk>/", TeacherDashboardView.as_view(), name="teacher-dashboard"),
]

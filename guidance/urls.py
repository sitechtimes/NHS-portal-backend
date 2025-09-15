from django.urls import path
from .views import *

urlpatterns = [
    path("student-view/<int:pk>/", StudentView.as_view(), name="view-student"),
    path(
        "expanded-student-view/<int:pk>/",
        ExpandedStudentView.as_view(),
        name="expanded-student-view",
    ),
    path(
        "multiple-students-view/",
        MultipleStudentsView.as_view(),
        name="multiple-students-view",
    ),
    path(
        "filter-students-view/",
        FilterStudentsView.as_view(),
        name="filter-students-view",
    ),
    path(
        "all-students-view/",
        AllStudentsView.as_view(),
        name="all-students-view",
    ),
    path(
        "give-recommendation/", GiveRecommendation.as_view(), name="give-recommendation"
    ),
    path(
        "create-announcement/",
        CreateAnnouncement.as_view(),
        name="create-announcement",
    ),
    path("announcements/", AnnouncementView.as_view(), name="announcements"),
    path(
        "create-biographical-question/",
        CreateBiographicalQuestion.as_view(),
        name="create-biographical-question",
    ),
    path(
        "biographical-questions/",
        BiographicalQuestionsView.as_view(),
        name="biographical-questions",
    ),
    path(
        "submit-question-instance/<int:pk>/",
        SubmitQuestionInstanceView.as_view(),
        name="submit-question-instance",
    ),
]

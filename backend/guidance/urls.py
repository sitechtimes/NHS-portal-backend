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
]

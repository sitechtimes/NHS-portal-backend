"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path
from users.views import *
from profiles.views import *
from guidance.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "profiles/create-service-activity/",
        CreateServiceActivity.as_view(),
        name="create=service-activity",
    ),
    path(
        "profiles/delete-service-activity/<int:pk>/",
        DeleteServiceActivity.as_view(),
        name="delete=service-activity",
    ),
    path(
        "profiles/update-service-activity/<int:pk>/",
        UpdateServiceActivity.as_view(),
        name="update-service-activity",
    ),
    path(
        "profiles/create-leadership-activity/",
        CreateLeadershipActivity.as_view(),
        name="create=leadership-activity",
    ),
    path(
        "profiles/delete-leadership-activity/<int:pk>/",
        DeleteLeadershipActivity.as_view(),
        name="delete=leadership-activity",
    ),
    path(
        "profiles/update-leadership-activity/<int:pk>/",
        UpdateLeadershipActivity.as_view(),
        name="update-leadership-activity",
    ),
    path(
        "profiles/update-service-profile/<int:pk>/",
        UpdateServiceProfile.as_view(),
        name="update-service-profile",
    ),
    path(
        "profiles/update-leadership-profile/<int:pk>/",
        UpdateLeadershipProfile.as_view(),
        name="update-leadership-profile",
    ),
    path("users/create-user/", CreateUser.as_view(), name="create-user"),
    path("users/delete-user/<int:pk>/", DeleteUser.as_view(), name="delete-user"),
    path("guidance/student-view/<int:pk>/", StudentView.as_view(), name="view-student"),
    path(
        "guidance/expanded-student-view/<int:pk>/",
        ExpandedStudentView.as_view(),
        name="expanded-student-view",
    ),
    path(
        "guidance/multiple-students-view/",
        MultipleStudentsView.as_view(),
        name="multiple-students-view",
    ),
    path(
        "guidance/filter-students-view/",
        FilterStudentsView.as_view(),
        name="filter-students-view",
    ),
    path(
        "guidance/all-students-view/",
        AllStudentsView.as_view(),
        name="all-students-view",
    ),
]

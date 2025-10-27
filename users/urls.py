from .views import GetUserView
from django.urls import path

urlpatterns = [
    path("get-user/", GetUserView.as_view(), name="get-user"),
]

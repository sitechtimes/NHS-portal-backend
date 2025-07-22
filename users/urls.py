from django.urls import path
from .views import *

urlpatterns = [
    path("create-user/", CreateUser.as_view(), name="create-user"),
    path("delete-user/<int:pk>/", DeleteUser.as_view(), name="delete-user"),
]

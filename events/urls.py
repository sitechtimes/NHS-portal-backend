from django.urls import path
from .views import *

urlpatterns = [
    path("create-event/", CreateEventView.as_view(), name="create-event"),
]

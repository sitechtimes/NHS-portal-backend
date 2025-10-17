from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
import requests

User = get_user_model()


class BackendTestCase(APITestCase):

    def setUp(self):
        base_url = "http://127.0.0.1:8000"
        self.auth_tokens = {
            "student": requests.post(
                "api/token/",
                data={"email": "bogdans3@nycstudents.net", "password": "password"},
            ),
            "teacher": requests.post(
                "api/token/",
                data={"email": "teacher1@gmail.com", "password": "password"},
            ),
            "guidance": requests.post(
                "api/token/",
                data={"email": "guidance@gmail.com", "password": "password"},
            ),
            "admin": requests.post(
                "api/token/", data={"email": "admin@gmail.com", "password": "password"}
            ),
        }

    def test_api_token(self):
        print(self.auth_tokens)

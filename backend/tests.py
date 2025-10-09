from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthTests(APITestCase):
    def test_access_token(self):
        data = {"email": "teacher1@gmail.com", "password": "password"}
        response = self.client.post("/api/token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        access_data = {"email": "teacher1@gmail.com", "password": "password"}
        access_response = self.client.post("/api/token/", access_data, format="json")

        refresh_data = {"refresh": access_response.data["refresh"]}
        refresh_response = self.client.post(
            "/api/token/refresh/", refresh_data, format="json"
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)

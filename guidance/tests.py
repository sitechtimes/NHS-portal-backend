from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


class StudentViewsTest(APITestCase):
    def setUp(self):
        email = "guidance@gmail.com"
        password = "password"
        access_token = self.client.post(
            "/api/token/", {"email": email, "password": password}
        ).data["access"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_student_view(self):
        url = "/guidance/students/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_multiple_students_view(self):
        url = "/guidance/students/?ids=[1,2,3]"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_students_view(self):
        url = "/guidance/students/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_students_view(self):
        url = "/guidance/students/?first_name=John"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expanded_student_view(self):
        url = "/guidance/students/1/expanded/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AnnouncementViewsTest(APITestCase):
    def setUp(self):
        email = "guidance@gmail.com"
        password = "password"
        access_token = self.client.post(
            "/api/token/", {"email": email, "password": password}
        ).data["access"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_create_announcement_view(self):
        url = "/guidance/announcements/"
        response = self.client.post(
            url,
            {
                "title": "Sample Announcement 3",
                "message": "This is a test message for the announcement 3.",
                "recipient_emails": ["sam.kipnis@gmail.com"],
                "send_immediately": True,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_announcement_view(self):
        self.client.post(
            "/guidance/announcements/",
            {
                "title": "Sample Announcement 3",
                "message": "This is a test message for the announcement 3.",
                "recipient_emails": ["sam.kipnis@gmail.com"],
                "send_immediately": True,
            },
        )
        url = "/guidance/announcements/1/"
        response = self.client.delete(url)
        self.assertIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_204_NO_CONTENT],
        )

    def test_all_announcements_view(self):
        url = "/guidance/announcements/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

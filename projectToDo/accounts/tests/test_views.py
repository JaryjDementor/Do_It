from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from django.test import Client


class ViewTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            username="TestUser", password="12345678Pas", email="test@gmail.com"
        )
        test_user.save()

    def test_first_page(self):
        c = Client()
        response = c.get("")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_register_request_uncorrect_request(self):
        c = Client()
        response = c.post(
            "/register",
            {
                "first_name": "Tom",
                "last_name": "Rich",
                "username": "TestUser",
                "email": "example",
                "password": "12345678Pas",
                "password2": "",
            },
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_register_request_current_email(self):
        c = Client()
        response = c.post(
            "/register",
            {
                "first_name": "Tom",
                "last_name": "Rich",
                "username": "TestUser",
                "email": "test@gmail.com",
                "password": "12345678Pas",
                "password2": "12345678Pas",
            },
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_register_request_correct_request(self):
        c = Client()
        response = c.post(
            "/register",
            {
                "first_name": "Tom",
                "last_name": "Rich",
                "username": "TestUser1",
                "email": "test1@gmail.com",
                "password1": "12345678Pas",
                "password2": "12345678Pas",
            },
        )
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_login_request_uncorrect_request(self):
        c = Client()
        response = c.post("/login", {"username": "TestUser", "password": "12345678"})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_login_request_correct_request(self):
        c = Client()
        response = c.post("/login", {"username": "TestUser", "password": "12345678Pas"})
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_logout_request(self):
        c = Client()
        response = c.get("/logout")
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

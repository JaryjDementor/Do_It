from unittest import TestCase
from django.test import Client
from django.contrib.auth import authenticate
from rest_framework import status


class TestRestToDo(TestCase):
    def test_get(self):
        c = Client()
        user = authenticate(username="TestAdmin", password="12345678Pas")
        c.force_login(user)
        response = c.get("/rest/api/v1/workerslist")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


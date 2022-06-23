from django.test import TestCase
from ..forms import NewUserForm


class FormTestCase(TestCase):
    def test_NewUserForm(self):
        form_data = {
            "first_name": "Tom",
            "last_name": "Rich",
            "username": "Test1",
            "email": "test1@gmail.com",
            "password1": "12345678Pas",
            "password2": "12345678Pas",
        }
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())

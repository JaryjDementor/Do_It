from django.test import TestCase
from ..forms import WorkersForm, NewTaskForm, TeamsListForm


class FormTestCase(TestCase):
    def test_WorkersForm(self):
        form_data = {
            "username": "Test1",
        }
        form = WorkersForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_NewTaskForm(self):
        form_data = {
            "description": 'Create presentation about Marketing',
            "categories": 'Marketing',
            "date_of_completion": "2022-06-09 00:00:00"
        }
        form = NewTaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_TeamsListForm(self):
        form_data = {
            "name_team": 'Marketing'
        }
        form = TeamsListForm(data=form_data)
        self.assertTrue(form.is_valid())
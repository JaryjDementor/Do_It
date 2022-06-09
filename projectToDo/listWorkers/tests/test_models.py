from datetime import datetime
from django.test import TestCase
from ..models import Workers, Employees_Task_List, TeamsList


class NotebookTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        notebook = Workers.objects.create(id_team="1", id_admin="2", id_worker="3", username="UserA", first_name='Tom', last_name='Rich')

    def test_id_team_label(self):
        notebook = Workers.objects.get(id=1)
        field_label = notebook._meta.get_field("id_team").verbose_name
        self.assertEquals(field_label, "id_team")

    def test_id_admin_label(self):
        notebook = Workers.objects.get(id=1)
        field_label = notebook._meta.get_field("id_admin").verbose_name
        self.assertEquals(field_label, "id_admin")

    def test_id_worker_label(self):
        notebook = Workers.objects.get(id=1)
        field_label = notebook._meta.get_field("id_worker").verbose_name
        self.assertEquals(field_label, "id_worker")

    def test_username_label(self):
        notebook = Workers.objects.get(id=1)
        field_label = notebook._meta.get_field("username").verbose_name
        self.assertEquals(field_label, "username")

    def test_first_name_label(self):
        notebook = Workers.objects.get(id=1)
        field_label = notebook._meta.get_field("first_name").verbose_name
        self.assertEquals(field_label, "first_name")

    def test_last_name_label(self):
        notebook = Workers.objects.get(id=1)
        field_label = notebook._meta.get_field("last_name").verbose_name
        self.assertEquals(field_label, "last_name")


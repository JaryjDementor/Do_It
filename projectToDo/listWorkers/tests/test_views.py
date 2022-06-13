from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from django.test import Client
from ..models import Employees_Task_List, TeamsList, Workers


class ViewListWorkersTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            first_name='Tom', last_name='Evans', username="TestUser", password="12345678Pas", email="test@gmail.com"
        )
        test_user.save()

        test_admin = User.objects.create_user(
            first_name='Robert', last_name='Petis', username="TestAdmin", password="12345678Pas", email="testadmin@gmail.com"
        )
        test_admin.save()

        test_user_2 = User.objects.create_user(
            first_name='Ron', last_name='Gor', username="TestUser_2", password="12345678Pas", email="test_2@gmail.com"
        )
        test_user_2.save()

        test_team_list = TeamsList.objects.create(
            name_team="TestTeam_1", id_admin="2"
        )
        test_team_list.save()

        test_workers = Workers.objects.create(
            id_team="1", id_admin="2", id_worker="1", username="TestUser", first_name="Tom", last_name="Evans"
        )
        test_workers.save()

        test_tasks_list = Employees_Task_List.objects.create(
            id_creator="2", id_worker="1", id_team="1", description="Create new Django project.", status="Not complete", categories="django", date_of_completion="2022-06-23 00:00:00"
        )
        test_tasks_list.save()

    def test_tasks_list(self):
        c = Client()
        user = authenticate(username="TestAdmin", password="12345678Pas")
        c.force_login(user)
        response = c.post("/tasks/")
        teams = TeamsList.objects.filter(id_admin=2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            list(teams.values_list("name_team")),
            [('TestTeam_1',)],
        )

    def test_create_new_team_delete_team(self):
        c = Client()
        user = authenticate(username="TestAdmin", password="12345678Pas")
        c.force_login(user)
        response = c.post(
            "/tasks/create-new-team/2",
            {
                            "id_admin": "2",
                            "name_team": "Test_Team_2",
                        }
        )
        team = TeamsList.objects.get(id="2")
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertEqual(team.id, 2)
        self.assertEqual(team.name_team, "Test_Team_2")

        response2 = c.post("/tasks/delete/2")
        team_delete = TeamsList.objects.filter(id=2)
        self.assertEqual(list(team_delete), [])
        self.assertEqual(status.HTTP_302_FOUND, response2.status_code)

    def test_list_workers(self):
        c = Client()
        user = authenticate(username="TestAdmin", password="12345678Pas")
        c.force_login(user)
        response = c.post("/tasks/list-workers/1")
        employees = Workers.objects.filter(id_team=1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            list(employees.values_list("username")),
            [('TestUser',)]
        )

    def test_add_an_employee_delete_worker(self):
        c = Client()
        user = authenticate(username="TestAdmin", password="12345678Pas")
        c.force_login(user)
        response = c.post(
            "/tasks/add-an-employee/1",
            {"username": "TestUser_2"},
        )
        employee = Workers.objects.get(username="TestUser_2")
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertEqual(employee.id, 2)
        self.assertEqual(employee.first_name, "Ron")

        response2 = c.post("/tasks/2/1/delete")
        employee_delete = Workers.objects.filter(username='TestUser_2')
        self.assertEqual(list(employee_delete), [])
        self.assertEqual(status.HTTP_302_FOUND, response2.status_code)
#
#     def test_Notebook_name_Update(self):
#         notebook = Notebook.objects.get(id=1)
#         c = Client()
#         user = authenticate(username="TestUser", password="12345678Pas")
#         c.force_login(user)
#         response = c.post(
#             "/accounts/notebook/1/update",
#             {"name_notebook": "TestNotebookEdit", "iduser": "1"},
#         )
#         edit_notebook = Notebook.objects.get(id=1)
#         self.assertEqual(notebook.name_notebook, "TestNotebook")
#         self.assertEqual(edit_notebook.name_notebook, "TestNotebookEdit")
#         self.assertEqual(status.HTTP_302_FOUND, response.status_code)
#
#
# class ViewNoteTestCase(TestCase):
#     def setUp(self):
#         test_user = User.objects.create_user(
#             username="TestUser", password="12345678Pas", email="test@gmail.com"
#         )
#         test_user.save()
#         test_user_2 = User.objects.create_user(
#             username="TestUser_2", password="12345678Pas_2", email="test_2@gmail.com"
#         )
#         test_user_2.save()
#
#         test_notebook = Notebook.objects.create(
#             name_notebook="TestNotebook", iduser="1"
#         )
#         test_notebook.save()
#         test_notebook_2 = Notebook.objects.create(
#             name_notebook="TestNotebook_2", iduser="2"
#         )
#         test_notebook_2.save()
#
#         test_note = Note.objects.create(
#             title="TestTitle",
#             text="Hallo world!!!",
#             data="2022-04-27 15:09:40.669876+00:00",
#             iduser="1",
#             id_notebook="2",
#         )
#         test_note.save()
#         test_note_2 = Note.objects.create(
#             title="TestTitle_2",
#             text="Peace",
#             data="2022-04-27 15:08:45.145466+00:00",
#             iduser="3",
#             id_notebook="4",
#         )
#         test_note_2.save()
#
#     def test_viewes_notebook(self):
#         c = Client()
#         user = authenticate(username="TestUser", password="12345678Pas")
#         c.force_login(user)
#         response = c.post("/accounts/notebook/2")
#         response_2 = c.post("/accounts/notebook/1")
#         note = Note.objects.get(iduser=1)
#         self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
#         self.assertEqual(status.HTTP_200_OK, response_2.status_code)
#         self.assertEqual("TestTitle", note.title)
#
#     def test_Note_Update(self):
#         c = Client()
#         user = authenticate(username="TestUser", password="12345678Pas")
#         c.force_login(user)
#         note = Note.objects.get(iduser=1)
#         response = c.post(
#             "/accounts/view_note/2/1/update",
#             {
#                 "title": "TestTitleEdit",
#                 "text": "Hallo world!!! Edit",
#                 "data": "2022-04-27 15:09:40.669876+00:00",
#                 "iduser": "1",
#                 "id_notebook": "2",
#             },
#         )
#         note_edit = Note.objects.get(iduser=1)
#         self.assertEqual([note.title, note.text], ["TestTitle", "Hallo world!!!"])
#         self.assertEqual(
#             [note_edit.title, note_edit.text], ["TestTitleEdit", "Hallo world!!! Edit"]
#         )
#         self.assertEqual(status.HTTP_302_FOUND, response.status_code)
#
#     def test_create_delete_note(self):
#         c = Client()
#         user = authenticate(username="TestUser", password="12345678Pas")
#         c.force_login(user)
#         response = c.post(
#             "/accounts/create/1",
#             {
#                 "title": "CreateTitle",
#                 "text": "Create Hallo world!!!",
#                 "data": "2022-04-27 15:11:40.669876+00:00",
#                 "iduser": "1",
#                 "id_notebook": "2",
#             },
#         )
#         note_create = Note.objects.get(id=3)
#         self.assertEqual(
#             [note_create.title, note_create.text],
#             ["CreateTitle", "Create Hallo world!!!"],
#         )
#         self.assertEqual(status.HTTP_302_FOUND, response.status_code)
#
#         response2 = c.post("/accounts/delete_note/2/3")
#         note_delete = Note.objects.filter(id=3)
#         self.assertEqual(status.HTTP_302_FOUND, response2.status_code)
#         self.assertEqual([], list(note_delete))
#
#     def test_view_your_note_check_log(self):
#         c = Client()
#         user = authenticate(username="TestUser", password="12345678Pas")
#         c.force_login(user)
#         response = c.get("/accounts/view_note/2/1")
#         response_2 = c.get("/accounts/view_note/4/2")
#         note = Note.objects.get(id=1)
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(["TestTitle", "Hallo world!!!"], [note.title, note.text])
#         self.assertEqual(status.HTTP_403_FORBIDDEN, response_2.status_code)

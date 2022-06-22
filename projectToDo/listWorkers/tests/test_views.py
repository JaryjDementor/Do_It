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

        response2 = c.post("/tasks/3/1/delete")
        employee_delete = Workers.objects.filter(username='TestUser_2')
        self.assertEqual(list(employee_delete), [])
        self.assertEqual(status.HTTP_302_FOUND, response2.status_code)

    def test_TaskList(self):
        c = Client()
        user = authenticate(username="TestAdmin", password="12345678Pas")
        c.force_login(user)
        response_post = c.post(
            "/tasks/1/1",
            {"description": "Create task 2", "categories": "Django", "date_of_completion": "2022-06-29 00:00:00"},
        )
        tasks_create = Employees_Task_List.objects.filter(id=2)
        response_get = c.get("/tasks/1/1", )
        tasks_employee = Employees_Task_List.objects.filter(id_worker=1)

        self.assertEqual(str(tasks_create) ,'<QuerySet [<Employees_Task_List:  Create task 2 Not complete Django 2022-06-29 00:00:00+00:00>]>')
        self.assertEqual(status.HTTP_200_OK, response_post.status_code)
        self.assertEqual(str(tasks_employee), '<QuerySet [<Employees_Task_List:  Create new Django project. Not complete django 2022-06-23 00:00:00+00:00>, <Employees_Task_List:  Create task 2 Not complete Django 2022-06-29 00:00:00+00:00>]>')
        self.assertEqual(status.HTTP_200_OK, response_get.status_code)

    def test_TaskComplete(self):
        c = Client()
        user = authenticate(username="TestUser", password="12345678Pas")
        c.force_login(user)
        response_post = c.post("/tasks/1/completed/")
        task_complete = Employees_Task_List.objects.filter(id=1)
        for i in task_complete:
            status_task = i.status

        self.assertEqual(status_task, 'Completed')
        self.assertEqual(status.HTTP_200_OK, response_post.status_code)

    def test_TaskDelete(self):
        c = Client()
        user = authenticate(username="TestUser", password="12345678Pas")
        c.force_login(user)
        response_post = c.post("/tasks/1/delete/")
        task_delete = Employees_Task_List.objects.filter(id=1)

        self.assertEqual(str(task_delete), '<QuerySet []>')
        self.assertEqual(status.HTTP_200_OK, response_post.status_code)

    def test_MyTasks(self):
        c = Client()
        user = authenticate(username="TestUser", password="12345678Pas")
        c.force_login(user)
        response_post = c.post("/tasks/my-tasks/1", {"description": "Create task 2", "categories": "Django", "date_of_completion": "2022-06-29 00:00:00"})
        response_get = c.get("/tasks/my-tasks/1")
        task_employee = Employees_Task_List.objects.filter(id_worker=1)

        self.assertEqual(str(task_employee), '<QuerySet [<Employees_Task_List:  Create new Django project. Not complete django 2022-06-23 00:00:00+00:00>, <Employees_Task_List:  Create task 2 Not complete Django 2022-06-29 00:00:00+00:00>]>')
        self.assertEqual(status.HTTP_200_OK, response_post.status_code)
        self.assertEqual(status.HTTP_200_OK, response_get.status_code)

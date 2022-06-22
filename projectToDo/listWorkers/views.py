from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.views import View
from .forms import WorkersForm, NewTaskForm, TeamsListForm
from .models import Workers, Employees_Task_List, TeamsList
from django.http import JsonResponse, HttpResponse
import csv

def check_log(id_user): #test
    if id_user:
        pass
    else:
        raise PermissionDenied()

def profile_user(request): #test
    iduser = request.user.id
    check_log(iduser)
    teams = TeamsList.objects.filter(id_admin=iduser)
    return render(request, "listWorkers/profile_user.html", {'teams':teams, 'id': iduser})

def create_new_team(request, iduser): #test
    iduser = request.user.id
    check_log(iduser)
    if request.method == "POST":
        form = TeamsListForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.id_admin = iduser
            order.save()
            return redirect("profile_user")
    form = TeamsListForm()
    return render(request, "listWorkers/create_new team.html", {"form": form})


def list_workers(request, id_team): #test
    iduser = request.user.id
    check_log(iduser)
    nameteam = TeamsList.objects.filter(id=id_team)
    info_admin='a'
    for i in nameteam:
        info_admin = i.id_admin
    name_admin = User.objects.filter(id=info_admin)
    db = Workers.objects.filter(id_team=id_team)
    a=[]
    data = {"db": db, 'a': a, 'id_team': id_team, 'nameteam': nameteam, 'name_admin': name_admin}
    return render(request, "listWorkers/list_workers.html", context=data)

def add_an_employee(request, id_team): #test
    iduser = request.user.id
    check_log(iduser)
    if request.method == "POST":
        form = WorkersForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            user = User.objects.filter(username=order.username)
            if user:
                for i in user:
                    order.id_worker = i.id
                    order.first_name = i.first_name
                    order.last_name = i.last_name
                order.id_team = id_team
                order.id_admin = iduser
                order.save()
                return redirect("list_workers", id_team)
    form = WorkersForm()
    return render(request, "listWorkers/add_worker.html", {"form": form, 'id_team': id_team})


class MyTasks(View): #test
    def get(self, request, iduser):
        id_user = request.user.id
        check_log(id_user)
        form = NewTaskForm()
        tasks = Employees_Task_List.objects.filter(id_worker=iduser)
        return render(
            request,
            "listWorkers/my_tasks.html",
            {"form": form, "tasks": tasks, "id_worker": iduser},
        )
    def post(self, request, iduser):
        id_user = request.user.id
        check_log(id_user)
        form = NewTaskForm(request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.id_creator = id_user
            new_task.id_worker = iduser
            new_task.id_team = iduser
            new_task.status = "Not complete"
            new_task.save()
            return JsonResponse({"task": model_to_dict(new_task)}, status=200)
        else:
            return redirect("my_tasks", iduser)


class TaskList(View): #test
    def get(self, request, id_team, id_worker):
        iduser = request.user.id
        check_log(iduser)
        form = NewTaskForm()
        tasks = Employees_Task_List.objects.filter(id_worker=id_worker)
        return render(
            request,
            "listWorkers/detail_worker_create_task.html",
            {"form": form, "tasks": tasks, "id_worker": id_worker, "id_team": id_team},
        )

    def post(self, request, id_team, id_worker):
        id_user = request.user.id
        check_log(id_user)
        form = NewTaskForm(request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.id_creator = id_user
            new_task.id_worker = id_worker
            new_task.id_team = id_team
            new_task.status = "Not complete"
            new_task.save()
            return JsonResponse({"task": model_to_dict(new_task)}, status=200)
        else:
            return redirect("task_list_url")


class TaskComplete(View): #test
    def post(self, request, id):
        iduser = request.user.id
        check_log(iduser)
        task = Employees_Task_List.objects.get(id=id)
        task.status = "Completed"
        task.save()
        task.completed = True
        return JsonResponse({"task": model_to_dict(task)}, status=200)


class TaskDelete(View): #test
    def post(self, request, id):
        iduser = request.user.id
        check_log(iduser)
        task = Employees_Task_List.objects.get(id=id)
        task.delete()
        return JsonResponse({"result": "ok"}, status=200)



def exportcsv(request, id_worker):
    employee_tasks = Employees_Task_List.objects.filter(id_worker=id_worker)
    response = HttpResponse("workersTask/csv")
    response["Content-Disposition"] = "attachment; filename=tasksWorker.csv"
    writer = csv.writer(response)
    writer.writerow(["Status", "Id", "Description", "Categories", "Date of completion"])
    tasks = employee_tasks.values_list(
        "status", "id", "description", "categories", "date_of_completion"
    )
    for task in tasks:
        writer.writerow(task)
    return response

def delete_worker(request, id_worker, id_team): #test
    del_em_task_list = Employees_Task_List.objects.filter(id_worker=id_worker, id_team=id_team).delete()
    telete_from_workers = Workers.objects.filter(id_worker=id_worker, id_team=id_team).delete()
    return redirect('list_workers', id_team)

def delete_team(request, id_team): #test
    del_from_team_list = TeamsList.objects.filter(id=id_team).delete()
    return redirect('profile_user')

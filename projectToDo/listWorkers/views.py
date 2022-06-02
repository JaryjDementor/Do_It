from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.views import View
from .forms import WorkersForm, NewTaskForm, TeamsListForm
from .models import Workers, Employees_Task_List, TeamsList
from django.http import JsonResponse, HttpResponse
import csv

def check_log(id_user):
    if id_user:
        pass
    else:
        raise PermissionDenied()

def profile_user(request):
    iduser = request.user.id
    check_log(iduser)
    teams = TeamsList.objects.filter(id_admin=iduser)
    return render(request, "listWorkers/profile_user.html", {'teams':teams, 'id': iduser})

def create_new_team(request, iduser):
    # id_user = request.user.id
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


def list_workers(request, id_team):
    iduser = request.user.id
    check_log(iduser)
    nameteam = TeamsList.objects.filter(id=id_team)
    # info_admin = User.objects.filter(id=nameteam.id_admin)
    info_admin='a'
    for i in nameteam:
        info_admin = i.id_admin
    name_admin = User.objects.filter(id=info_admin)
    db = Workers.objects.filter(id_team=id_team)
    a=[]

    # info_employee = User.objects.filter(id=db.id_worker)
    data = {"db": db, 'a': a, 'id_team': id_team, 'nameteam': nameteam, 'name_admin': name_admin}
    return render(request, "listWorkers/list_workers.html", context=data)

def add_an_employee(request, id_team):
    iduser = request.user.id
    check_log(iduser)
    bd = TeamsList.objects.filter(id=id_team)
    if request.method == "POST":
        form = WorkersForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.id_team = id_team
            user = User.objects.get(username=order.username)
            order.id_worker = user.id
            order.first_name = user.first_name
            order.last_name = user.last_name
            order.save()
            return redirect("list_workers", id_team)
    form = WorkersForm()
    return render(request, "listWorkers/add_worker.html", {"form": form})




class TaskList(View):
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
        iduser = request.user.id
        check_log(iduser)
        form = NewTaskForm(request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.id_worker = id_worker
            new_task.id_team = id_team
            new_task.status = "Not complete"
            new_task.save()
            return JsonResponse({"task": model_to_dict(new_task)}, status=200)
        else:
            return redirect("task_list_url")





class TaskComplete(View):
    def post(self, request, id):
        iduser = request.user.id
        check_log(iduser)
        task = Employees_Task_List.objects.get(id=id)
        task.status = "Completed"
        task.save()
        task.completed = True
        return JsonResponse({"task": model_to_dict(task)}, status=200)


class TaskDelete(View):
    def post(self, request, id):
        iduser = request.user.id
        check_log(iduser)
        task = Employees_Task_List.objects.get(id=id)
        task.delete()
        return JsonResponse({"result": "ok"}, status=200)


class SortTaskListStatus(View):
    def get(self, request, id_team, id_worker):
        iduser = request.user.id
        check_log(iduser)
        form = NewTaskForm()
        tasks = Employees_Task_List.objects.filter(id_worker=id_worker).order_by(
            "-status"
        )
        return render(
            request,
            "listWorkers/detail_worker_create_task.html",
            {"form": form, "tasks": tasks, "id_worker": id_worker, 'id_team': id_team},
        )

    def post(self, request, id_team, id_worker):
        iduser = request.user.id
        check_log(iduser)
        form = NewTaskForm(request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.status = "Not complete"
            new_task.id_worker = id_worker
            new_task.save()
            return JsonResponse({"task": model_to_dict(new_task)}, status=200)
        else:
            return redirect("task_list_url")


class SortTaskListDate(View):
    def get(self, request, id_team, id_worker):
        iduser = request.user.id
        check_log(iduser)
        form = NewTaskForm()
        tasks = Employees_Task_List.objects.filter(id_worker=id_worker).order_by(
            "date_of_completion"
        )
        return render(
            request,
            "listWorkers/detail_worker_create_task.html",
            {"form": form, "tasks": tasks, "id_worker": id_worker, 'id_team': id_team},
        )

    def post(self, request, id_worker):
        iduser = request.user.id
        check_log(iduser)
        form = NewTaskForm(request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.status = "Not complete"
            new_task.id_worker = id_worker
            new_task.save()
            return JsonResponse({"task": model_to_dict(new_task)}, status=200)
        else:
            return redirect("task_list_url")


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

def delete_worker(request, id_worker):
    a=Employees_Task_List.objects.filter(id_worker=id_worker).delete()
    b=Workers.objects.filter(id=id_worker).delete()
    return redirect('list_workers')

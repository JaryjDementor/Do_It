from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.views import View
from .forms import NewWorkerForm, NewTaskForm
from .models import Workers, Employees_Task_List
from django.http import JsonResponse, HttpResponse
import csv


def first_page(request):
    return render(request, "listWorkers/first_page.html")


def list_workers(request):
    db = Workers.objects.all()
    data = {"db": db}
    return render(request, "listWorkers/list_workers.html", context=data)


def create_new_worker(request):
    if request.method == "POST":
        form = NewWorkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_workers")
    form = NewWorkerForm()
    return render(request, "listWorkers/create_new_worker.html", {"form": form})


class TaskList(View):
    def get(self, request, id_worker):
        form = NewTaskForm()
        tasks = Employees_Task_List.objects.filter(idworker=id_worker)
        return render(
            request,
            "listWorkers/detail_worker_create_task.html",
            {"form": form, "tasks": tasks, "id_worker": id_worker},
        )

    def post(self, request, id_worker):
        form = NewTaskForm(request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.idworker = id_worker
            new_task.status = "Not complete"
            new_task.save()
            return JsonResponse({"task": model_to_dict(new_task)}, status=200)
        else:
            return redirect("task_list_url")


class TaskComplete(View):
    def post(self, request, id):
        task = Employees_Task_List.objects.get(id=id)
        task.status = "Completed"
        task.save()
        task.completed = True
        return JsonResponse({"task": model_to_dict(task)}, status=200)


class TaskDelete(View):
    def post(self, request, id):
        task = Employees_Task_List.objects.get(id=id)
        task.delete()
        return JsonResponse({"result": "ok"}, status=200)


class SortTaskListStatus(View):
    def get(self, request, id_worker):
        form = NewTaskForm()
        tasks = Employees_Task_List.objects.filter(idworker=id_worker).order_by(
            "-status"
        )
        return render(
            request,
            "listWorkers/detail_worker_create_task.html",
            {"form": form, "tasks": tasks, "id_worker": id_worker},
        )

    def post(self, request, id_worker):
        form = NewTaskForm(request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.status = "Not complete"
            new_task.idworker = id_worker
            new_task.save()
            return JsonResponse({"task": model_to_dict(new_task)}, status=200)
        else:
            return redirect("task_list_url")


class SortTaskListDate(View):
    def get(self, request, id_worker):
        form = NewTaskForm()
        tasks = Employees_Task_List.objects.filter(idworker=id_worker).order_by(
            "date_of_completion"
        )
        return render(
            request,
            "listWorkers/detail_worker_create_task.html",
            {"form": form, "tasks": tasks, "id_worker": id_worker},
        )

    def post(self, request, id_worker):
        form = NewTaskForm(request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.status = "Not complete"
            new_task.idworker = id_worker
            new_task.save()
            return JsonResponse({"task": model_to_dict(new_task)}, status=200)
        else:
            return redirect("task_list_url")


def exportcsv(request, id_worker):
    employee_tasks = Employees_Task_List.objects.filter(idworker=id_worker)
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

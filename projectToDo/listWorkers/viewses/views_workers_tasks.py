from ..forms import NewTaskForm
from ..models import Employees_Task_List
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.forms import model_to_dict

class TaskList(View):
    def get(self, request, id_team, id_worker):
        form = NewTaskForm()
        tasks = Employees_Task_List.objects.filter(id_worker=id_worker)
        return render(
            request,
            "listWorkers/detail_worker_create_task.html",
            {"form": form, "tasks": tasks, "id_worker": id_worker, "id_team": id_team},
        )

    def post(self, request, id_team, id_worker):
        id_user = request.user.id
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
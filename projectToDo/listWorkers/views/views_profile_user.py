from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import TeamsList, Employees_Task_List
from ..forms import TeamsListForm, NewTaskForm
from django.http import JsonResponse
from django.forms import model_to_dict
from django.views import View

@login_required
def profile_user(request):
    iduser = request.user.id
    teams = TeamsList.objects.filter(id_admin=iduser)
    return render(
        request, "listWorkers/profile_user.html", {"teams": teams, "id": iduser}
    )

@login_required
def create_new_team(request, iduser):
    if request.method == "POST":
        form = TeamsListForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.id_admin = iduser
            order.save()
            return redirect("profile_user")
    form = TeamsListForm()
    return render(request, "listWorkers/create_new team.html", {"form": form})


class MyTasks(View):

    def get(self, request, iduser):
        form = NewTaskForm()
        tasks = Employees_Task_List.objects.filter(id_worker=iduser)
        return render(
            request,
            "listWorkers/my_tasks.html",
            {"form": form, "tasks": tasks, "id_worker": iduser},
        )

    def post(self, request, iduser):
        id_user = request.user.id
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

class TaskComplete(View):

    def post(self, request, id):
        iduser = request.user.id
        # check_log(iduser)
        task = Employees_Task_List.objects.get(id=id)
        task.status = "Completed"
        task.save()
        task.completed = True
        return JsonResponse({"task": model_to_dict(task)}, status=200)

class TaskDelete(View):

    def post(self, request, id):
        # iduser = request.user.id
        # check_log(iduser)
        task = Employees_Task_List.objects.get(id=id)
        task.delete()
        return JsonResponse({"result": "ok"}, status=200)
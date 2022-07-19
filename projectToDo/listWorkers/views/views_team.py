from django.contrib.auth.decorators import login_required
from ..models import TeamsList, Workers
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from ..forms import WorkersForm

@login_required
def list_workers(request, id_team):
    nameteam = TeamsList.objects.filter(id=id_team)
    info_admin = None
    for i in nameteam:
        info_admin = i.id_admin
    name_admin = User.objects.filter(id=info_admin)
    db = Workers.objects.filter(id_team=id_team)
    data = {
        "db": db,
        "id_team": id_team,
        "nameteam": nameteam,
        "name_admin": name_admin,
    }
    return render(request, "listWorkers/list_workers.html", context=data)

@login_required
def add_an_employee(request, id_team):
    iduser = request.user.id
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
    return render(
        request, "listWorkers/add_worker.html", {"form": form, "id_team": id_team}
    )

def delete_team(request, id_team):
    TeamsList.objects.filter(id=id_team).delete()
    return redirect("profile_user")
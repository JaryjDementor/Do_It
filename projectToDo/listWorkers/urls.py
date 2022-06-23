from django.urls import path

from .views import (
    list_workers,
    TaskList,
    TaskComplete,
    TaskDelete,
    exportcsv,
    profile_user,
    delete_worker,
    create_new_team,
    add_an_employee,
    MyTasks,
    delete_team,
)

urlpatterns = [
    path("", profile_user, name="profile_user"),
    path("create-new-team/<int:iduser>", create_new_team, name="create_new_team"),
    path("list-workers/<int:id_team>", list_workers, name="list_workers"),
    path("add-an-employee/<int:id_team>", add_an_employee, name="add_an_employee"),
    path("my-tasks/<int:iduser>", MyTasks.as_view(), name="my_tasks"),
    path(
        "my-tasks/<str:id>/completed/", TaskComplete.as_view(), name="my_tasks_complete"
    ),
    path("<int:id_team>/<int:id_worker>", TaskList.as_view(), name="task_list_url"),
    path("<str:id>/completed/", TaskComplete.as_view(), name="task_complete_url"),
    path("<str:id>/delete/", TaskDelete.as_view(), name="task_delete_url"),
    path("<int:id_worker>/export-tasks", exportcsv, name="export_tasks"),
    path("<int:id_worker>/<int:id_team>/delete", delete_worker, name="delete_worker"),
    path("delete/<int:id_team>", delete_team, name="delete_team"),
]

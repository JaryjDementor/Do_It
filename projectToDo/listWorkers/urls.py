from django.urls import path

from .views import (
    list_workers,
    create_new_worker,
    TaskList,
    TaskComplete,
    TaskDelete,
    SortTaskListStatus,
    SortTaskListDate,
    exportcsv,
    first_page,
    delete_worker,
)

urlpatterns = [
    path("", first_page, name="first_page"),
    path("list-workers", list_workers, name="list_workers"),
    path("create-new-worker", create_new_worker, name="create_new_worker"),
    path("<int:id_worker>", TaskList.as_view(), name="task_list_url"),
    path("<str:id>/completed/", TaskComplete.as_view(), name="task_complete_url"),
    path("<str:id>/delete/", TaskDelete.as_view(), name="task_delete_url"),
    path(
        "<int:id_worker>/sort-status",
        SortTaskListStatus.as_view(),
        name="task_sortstatus_list_url",
    ),
    path(
        "<int:id_worker>/sort-date",
        SortTaskListDate.as_view(),
        name="task_sortdate_list_url",
    ),
    path("<int:id_worker>/export-tasks", exportcsv, name="export_tasks"),
    path("<int:id_worker>/delete", delete_worker, name="delete_worker"),
]

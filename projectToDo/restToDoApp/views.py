from listWorkers.models import Employees_Task_List, Workers
from .serializers import TasksWorkerSerializer, WorkersSerializer
from drf_multiple_model.views import ObjectMultipleModelAPIView
from datetime import date


class WorkersTasksAPIView(ObjectMultipleModelAPIView):
    querylist = [
        {"queryset": Workers.objects.all(), "serializer_class": WorkersSerializer},
        {
            "queryset": Employees_Task_List.objects.filter(
                date_of_completion=date.today()
            ),
            "serializer_class": TasksWorkerSerializer,
        },
    ]

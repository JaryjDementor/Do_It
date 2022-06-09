from listWorkers.models import Employees_Task_List, Workers, TeamsList
from .serializers import TasksWorkerSerializer, WorkersSerializer
from drf_multiple_model.views import ObjectMultipleModelAPIView
from datetime import date


class WorkersTasksAPIView(ObjectMultipleModelAPIView):
    def get_querylist(self):
        id = self.request.user.id
        querylist = [
            {"queryset": Workers.objects.filter(id_admin=id), "serializer_class": WorkersSerializer},
            {
                "queryset": Employees_Task_List.objects.filter(
                    date_of_completion=date.today(), id_creator=id
                ),
                "serializer_class": TasksWorkerSerializer,
            },
        ]
        return querylist

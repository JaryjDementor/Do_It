from rest_framework import serializers
from listWorkers.models import Employees_Task_List, Workers


class TasksWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees_Task_List
        fields = "__all__"


class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workers
        fields = "__all__"

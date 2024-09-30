from rest_framework import viewsets
from app.serilaizers.task_serializer import *

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskInfoViewSet(viewsets.ModelViewSet):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskInfoSerializer

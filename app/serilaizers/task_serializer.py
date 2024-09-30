from rest_framework import serializers
from app.models.task_model import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInfo
        fields = '__all__'
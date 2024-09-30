from rest_framework import serializers
from app.models.employee_model import *

class UserEmployeeSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserEmployee
    fields = '__all__'
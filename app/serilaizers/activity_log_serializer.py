from rest_framework import serializers
from app.models.activity_log_model import *

class ActivityLogSerializer(serializers.ModelSerializer):
  class Meta:
    model = ActivityLog
    fields = '__all__'
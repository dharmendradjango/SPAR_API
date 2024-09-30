from rest_framework import serializers
from app.models.job_model import *

class JobSerializer(serializers.ModelSerializer):
  class Meta:
    model = Job
    fields = '__all__'

    
class JobFrequencySerializer(serializers.ModelSerializer):
  class Meta:
    model = JobFrequency
    fields = '__all__'
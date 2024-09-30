from rest_framework import serializers
from app.models.client_model import *


class UserClientSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserClient
    fields = '__all__'

  

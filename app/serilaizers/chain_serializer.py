from rest_framework import serializers
from app.models.chain_model import *

class ChainSerializer(serializers.ModelSerializer):
  class Meta:
    model = Chain
    fields = '__all__'


class ChainStoreSerializer(serializers.ModelSerializer):
  class Meta:
    model = ChainStore
    fields = '__all__'

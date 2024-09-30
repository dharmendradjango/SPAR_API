from rest_framework import serializers
from app.models.store_model import *

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreMedia
        fields = '__all__'


class StoreProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreProduct
        fields = '__all__'
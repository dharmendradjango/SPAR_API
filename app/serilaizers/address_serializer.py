from rest_framework import serializers
from app.models.address_model import *

class StateSerializer(serializers.ModelSerializer):
  class Meta:
    model = State
    fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city', 'status', 'reg_date']

    def get_state(self, obj):
        try:
            state = State.objects.get(id=obj.state_id)
            return {
                "id": state.id,
                "name": state.name,
                "status": state.status,
                "reg_date": state.reg_date
            }
        except State.DoesNotExist:
            return None


class PincodeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Pincode
    fields = '__all__'


class ClientAddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = ClientAddress
    fields = '__all__'


class StoreAddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = StoreAddress
    fields = '__all__'

class UserClientAddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserClientAddress
    fields = '__all__'


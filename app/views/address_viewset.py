from django.db import connection
from rest_framework import viewsets,views,status
from app.serilaizers.address_serializer import *
from rest_framework.response import Response


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get(self, request, *args, **kwargs):
        state_id = self.kwargs.get('state_id')
        if state_id:
            queryset = self.get_queryset().filter(state_id=state_id)
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class PincodeViewSet(viewsets.ModelViewSet):
    queryset = Pincode.objects.all()
    serializer_class = PincodeSerializer


class UserClientAddressViewSet(viewsets.ModelViewSet):
    queryset = UserClientAddress.objects.all()
    serializer_class = UserClientAddressSerializer


class ClientAddressViewSet(views.APIView):
    def get(self, request, pk=None):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'error': 'user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
#         query = f''' 
#        select tuc.Name,tuc.GST,tuc.Mobile,tuc.Email,tc.Id,tc.address1,tc.address2,tc.name as state,tc.city,CASE WHEN tc.Status = 1 THEN 'Active' ELSE 'Inactive' END AS Status from tbl_user as tu
# join tbl_user_client as tuc on tuc.UID=tu.Id
# join(select tcd.Id,tcd.UID,tcd.address1,tcd.address2,ts.name,c.city,tcd.Status from tbl_client_address as tcd
# join tbl_state as ts on ts.Id=tcd.State 
# join tbl_city as c on c.Id=tcd.City) as tc on tu.Id=tc.UID 
# where tu.ID={user_id};
#         '''

        query = f''' 
SELECT tcd.*, ts.name AS State, c.city AS City, CASE WHEN tcd.Status = 1 THEN 'Active' ELSE 'Inactive' END AS Status FROM tbl_client_address tcd JOIN tbl_state ts ON ts.Id = tcd.State JOIN tbl_city c ON c.Id = tcd.City WHERE tcd.UID = {user_id};

        '''
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            if results:
                return Response(results)
            else:
                return Response(0)
    
    def post(self, request):
        pincode_id = request.data.get('pin_code')
        if pincode_id:
            client_address_serializer = ClientAddressSerializer(data=request.data)
            if client_address_serializer.is_valid():
                client_address_serializer.save()
                return Response({'msg': 'Data saved'}, status=status.HTTP_201_CREATED)
            else:
                return Response(client_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            pincode_value = request.data.get('pincode_code')
            pincode_serializer = PincodeSerializer(data={'code': pincode_value, 'status': 1})
            if pincode_serializer.is_valid():
                pincode_instance = pincode_serializer.save()
                request.data['pin_code'] = pincode_instance.id
                client_address_serializer = ClientAddressSerializer(data=request.data)
                if client_address_serializer.is_valid():
                    client_address_serializer.save()
                    return Response({'msg': 'Data saved'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(client_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(pincode_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        try:
            client_address = ClientAddress.objects.get(pk=pk)
        except ClientAddress.DoesNotExist:
            return Response({'error': 'ClientAddress not found'}, status=status.HTTP_404_NOT_FOUND)
        
        pincode_id = request.data.get('pin_code')
        if pincode_id:
            client_address_serializer = ClientAddressSerializer(client_address, data=request.data)
            if client_address_serializer.is_valid():
                client_address_serializer.save()
                return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
            else:
                return Response(client_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            pincode_value = request.data.get('pincode_code')
            pincode_serializer = PincodeSerializer(data={'code': pincode_value, 'status': 1})
            if pincode_serializer.is_valid():
                pincode_instance = pincode_serializer.save()
                request.data['pin_code'] = pincode_instance.id
                client_address_serializer = ClientAddressSerializer(client_address, data=request.data)
                if client_address_serializer.is_valid():
                    client_address_serializer.save()
                    return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
                else:
                    return Response(client_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(pincode_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            client_address = ClientAddress.objects.get(pk=pk)
        except ClientAddress.DoesNotExist:
            return Response({'error': 'ClientAddress not found'}, status=status.HTTP_404_NOT_FOUND)

        client_address.delete()
        return Response({'msg': 'Data deleted'}, status=status.HTTP_204_NO_CONTENT)


class StoreAddressViewSet(views.APIView):
    def get(self, request, pk=None):
        query = f''' 


        '''
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            if results:
                return Response(results)
            else:
                return Response(0)
    
    def post(self, request):
        pincode_id = request.data.get('pin_code')
        if pincode_id:
            store_address_serializer = StoreAddressSerializer(data=request.data)
            if store_address_serializer.is_valid():
                store_address_serializer.save()
                return Response({'msg': 'Data saved'}, status=status.HTTP_201_CREATED)
            else:
                return Response(store_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            pincode_value = request.data.get('pincode_code')
            pincode_serializer = PincodeSerializer(data={'code': pincode_value, 'status': 1})
            if pincode_serializer.is_valid():
                pincode_instance = pincode_serializer.save()
                request.data['pin_code'] = pincode_instance.id
                store_address_serializer = StoreAddressSerializer(data=request.data)
                if store_address_serializer.is_valid():
                    store_address_serializer.save()
                    return Response({'msg': 'Data saved'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(store_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(pincode_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        try:
            store_address = StoreAddress.objects.get(pk=pk)
        except StoreAddress.DoesNotExist:
            return Response({'error': 'StoreAddress not found'}, status=status.HTTP_404_NOT_FOUND)
        
        pincode_id = request.data.get('pin_code')
        if pincode_id:
            store_address_serializer = StoreAddressSerializer(store_address, data=request.data)
            if store_address_serializer.is_valid():
                store_address_serializer.save()
                return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
            else:
                return Response(store_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            pincode_value = request.data.get('pincode_code')
            pincode_serializer = PincodeSerializer(data={'code': pincode_value, 'status': 1})
            if pincode_serializer.is_valid():
                pincode_instance = pincode_serializer.save()
                request.data['pin_code'] = pincode_instance.id
                store_address_serializer = StoreAddressSerializer(store_address, data=request.data)
                if store_address_serializer.is_valid():
                    store_address_serializer.save()
                    return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
                else:
                    return Response(store_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(pincode_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            store_address = StoreAddress.objects.get(pk=pk)
        except StoreAddress.DoesNotExist:
            return Response({'error': 'StoreAddress not found'}, status=status.HTTP_404_NOT_FOUND)

        store_address.delete()
        return Response({'msg': 'Data deleted'}, status=status.HTTP_204_NO_CONTENT)
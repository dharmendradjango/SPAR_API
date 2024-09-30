# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import action
# from rest_framework.pagination import PageNumberPagination
# from rest_framework import status, permissions, authentication
# from app.utils.authentication import CustomTokenAuthentication
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model
from django.http import JsonResponse, StreamingHttpResponse, FileResponse
from django.db import connection
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serilaizers.client_serializer import *
from io import BytesIO  
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from django.http import FileResponse
from io import BytesIO
from app.models.address_model import *
from django.db import transaction
from app.serilaizers.extra_serializer import CustomToken, User
from app.serilaizers.login_serializer import UserSerializer
import datetime
from django.utils.timezone import is_aware, make_naive
from fpdf import FPDF 
from django.utils import timezone
from app.serilaizers import extra_serializer
from app.serilaizers.address_serializer import *



class UserClientViewSet(viewsets.ModelViewSet):
    queryset = UserClient.objects.all()
    serializer_class = UserClientSerializer
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     client_id = self.request.query_params.get('client_id', None)
    #     client_name = self.request.query_params.get('client_name', None)
    #     queryset = UserClient.objects.all()  
    #     if client_id is not None:
    #         client_id = int(client_id)
    #         queryset = queryset.filter(id=client_id)
    #     if client_name is not None:
    #         queryset = queryset.filter(name=client_name)
    #     return queryset
    
    # def list(self, request, *args, **kwargs): 
    #     queryset = self.get_queryset()
    #     response_data = []

    #     for employee in queryset:
    #         user = User.objects.filter(id=employee.uid).first()  # Manually fetch the user
    #         user_serializer = extra_serializer.UserSerializer(user)
    #         employee_serializer = UserClientSerializer(employee)

    #         response_data.append({
    #             "user": user_serializer.data if user else None,  # Handle case if no user is found
    #             "employee": employee_serializer.data
    #         })

    #     return Response(response_data, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     user_data = request.data.get('user', {})
    #     client_data = request.data

    #     # Validate and create the user
    #     user_serializer = UserSerializer(data=user_data)
    #     if user_serializer.is_valid():
    #         with transaction.atomic():
    #             user = user_serializer.save()

    #             # Generate a token for the user
    #             CustomToken.objects.filter(user=user).delete()  # Clean up any existing tokens
    #             token, _ = CustomToken.objects.get_or_create(user=user)

    #             # Set the uid in the client data to be the id of the created user
    #             client_data['uid'] = user.id

    #             # Create the UserClient entry
    #             client_serializer = UserClientSerializer(data=client_data)
    #             if client_serializer.is_valid():
    #                 user_client = client_serializer.save()

    #                 # Prepare the response data
    #                 response_data = {
    #                     "user": user_serializer.data,
    #                     "client": client_serializer.data,
    #                     "token": token.token_key
    #                 }

    #                 return Response(response_data, status=status.HTTP_201_CREATED)
    #             else:
    #                 return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientExcel(APIView):
    # def post(self, request):
    #     if request.method == 'POST' and 'file' in request.FILES:
    #         excel_file = request.FILES['file']
    #         fs = FileSystemStorage()
    #         filename = fs.save(excel_file.name, excel_file)
    #         file_path = fs.path(filename)

    #         try:
    #             df = pd.read_excel(file_path)

    #             df = df.fillna({
    #                 "Name": "",
    #                 "FullName": "",
    #                 "TradeName": "",
    #                 "GST": "",
    #                 "Code": "",
    #                 "Role": "",
    #                 "Type": "",
    #                 "Email": "",
    #                 "Mobile": "",
    #                 "PAN": "",
    #                 "CIN": "",
    #                 "INCDate": None,
    #                 "Description": "",
    #                 "Logo": "",
    #                 "UID": None,
    #                 "Status": False,
    #                 "RegDate": None,
    #             })

    #             client_instances = []
    #             for _, row in df.iterrows():
    #                 try:
    #                     city = None
    #                     if isinstance(row['City'], str):
    #                         city = City.objects.get(name=row['City'].capitalize())
    #                 except ObjectDoesNotExist:
    #                     city = None

    #                 try:
    #                     state = None
    #                     if isinstance(row['State'], str):
    #                         state = State.objects.get(name=row['State'].capitalize())
    #                 except ObjectDoesNotExist:
    #                     state = None

    #                 client_instance = UserClient(
    #                     name=row['Name'],
    #                     full_name=row['FullName'],
    #                     trade_name=row['TradeName'],
    #                     gst=row['GST'],
    #                     code=row['Code'],
    #                     role=row['Role'],
    #                     type=row['Type'],
    #                     email=row['Email'],
    #                     mobile=row['Mobile'],
    #                     pan=row['PAN'],
    #                     cin=row['CIN'],
    #                     inc_date=row['INCDate'],
    #                     description=row['Description'],
    #                     file=row['File'],
    #                     uid=row['UID'],
    #                     status=row['Status'],
    #                     reg_date=datetime.datetime.now()
    #                 )
    #                 client_instances.append(client_instance)

    #             UserClient.objects.bulk_create(client_instances)
    #             return Response({'message': 'File uploaded and data saved successfully'}, status=200)
    #         except Exception as e:
    #             return Response({'error': str(e)}, status=400)
    #     return Response({'error': 'Invalid request'}, status=400)

    def post(self, request):
        if request.method == 'POST' and 'file' in request.FILES:
            excel_file = request.FILES['file']
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return Response({'error': 'Invalid file format. Please upload an Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            file_path = fs.path(filename)

            try:
                df = pd.read_excel(file_path)

                # Ensure 'Status' column exists
                if "Status" not in df.columns:
                    df["Status"] = True

                fill_values = {
                    "Name": "",
                    "FullName": "",
                    "TradeName": "",
                    "GST": "",
                    "Code": "",
                    "Role": "",
                    "Type": "",
                    "Email": "",
                    "Mobile": "",
                    "PAN": "",
                    "CIN": "",
                    "INCDate": pd.NaT,
                    "Description": "",
                    "Status": True,
                    "FirstName": "",
                    "LastName": "",
                    "Username": "",
                    "Password": "",
                    "Password2": "",
                    "Address1": "",
                    "Address2": "",
                    "Street": "",
                    "Landmark": "",
                    "City": "",
                    "State": "",
                    "Country": "",
                    "PinCode": "",
                    "Latitude": "",
                    "Longitude": ""
                }
                df = df.fillna(value=fill_values)

                client_instances = []
                address_instances = []
                with transaction.atomic():
                    for _, row in df.iterrows():
                        city_id = None
                        if pd.notna(row['City']):
                            try:
                                city = City.objects.get(city=row['City'].capitalize())
                                city_id = city.id
                            except City.DoesNotExist:
                                pass 
                        state_id = None
                        if pd.notna(row['State']):
                            try:
                                state = State.objects.get(name=row['State'].capitalize())
                                state_id = state.id
                            except State.DoesNotExist:
                                pass  
                        pincode_id = None
                        if pd.notna(row['PinCode']):
                            try:
                                pincode = Pincode.objects.get(code=row['PinCode'])
                                pincode_id = pincode.id
                            except Pincode.DoesNotExist:
                                pincode = Pincode.objects.create(
                                    code=row['PinCode'],
                                    status=1,
                                    reg_date=timezone.now()
                                )
                                pincode_id = pincode.id

                        inc_date = row['INCDate']
                        if isinstance(inc_date, pd.Timestamp):
                            inc_date = inc_date.to_pydatetime().date()
                        else:
                            inc_date = None

                        user = User.objects.filter(username=row['Username']).first()
                       
                        if user is None:
                            user_data = {
                                "first_name": row['FirstName'],
                                "last_name": row['LastName'],
                                "email": row['Email'],
                                "mobile": row['Mobile'],
                                "username": row['Username'],
                                "password": row['Password'],
                                "password2": row['Password2'],
                                "role_id": 4,
                                "status": row['Status'],
                            }
                            user_serializer = UserSerializer(data=user_data)
                            if user_serializer.is_valid():
                                # user = user_serializer.save()
                                client_instance = UserClient(
                                    name=row['Name'],
                                    full_name=row['FullName'],
                                    trade_name=row['TradeName'],
                                    gst=row['GST'],
                                    code=row['Code'],
                                    role=row['Role'],
                                    type=row['Type'],
                                    email=row['Email'],
                                    mobile=row['Mobile'],
                                    pan=row['PAN'],
                                    cin=row['CIN'],
                                    inc_date=inc_date,
                                    description=row['Description'],
                                    # uid=user.id,  # Link the client to the created user
                                    status=row['Status'],
                                    reg_date=timezone.now()
                                )
                                client_instances.append(client_instance)
                            else:
                                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        address_instance = ClientAddress(
                            # uid= user.id,
                            address1= row['Address1'],
                            address2= row['Address2'],
                            street= row['Street'],
                            landmark= row['Landmark'],
                            city= city_id,
                            state= state_id,
                            country= row['Country'],
                            pin_code= pincode_id,
                            latitude= row['Latitude'],
                            longitude= row['Longitude'],
                            status= row['Status'],
                            reg_date= timezone.now()
                        )
                        address_instances.append(address_instance)
                        # Prepare address data
                        address_data = {
                            # "uid": user.id,
                            "address1": row['Address1'],
                            "address2": row['Address2'],
                            "street": row['Street'],
                            "landmark": row['Landmark'],
                            "city": city_id,
                            "state": state_id,
                            "country": row['Country'],
                            "pin_code": pincode_id,
                            "latitude": row['Latitude'],
                            "longitude": row['Longitude'],
                            "status": row['Status'],
                            "reg_date": timezone.now()
                        }
                        address_serializer = ClientAddressSerializer(data=address_data)
                        if address_serializer.is_valid():
                            address_instances.append(address_serializer.validated_data)
                        else:
                            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    # if client_instances:
                    #     UserClient.objects.bulk_create(client_instances)

                    if address_instances:
                        ClientAddress.objects.bulk_create(address_instances)


                    if address_instances:
                        ClientAddress.objects.bulk_create([ClientAddress(**data) for data in address_instances])

                    serializer = UserClientSerializer(client_instances, many=True)
                    address_serilizer = ClientAddressSerializer(address_instances,many=True)
                    return Response({
                        'message': 'File uploaded and data saved successfully',
                        'clients': serializer.data,
                        'address':address_serilizer.data
                    }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        clients = UserClient.objects.all().values(
            'id', 'name', 'full_name', 'trade_name', 'gst', 'code', 'role', 'type', 
            'email', 'mobile', 'pan', 'cin', 'inc_date', 'description', 'file', 'uid', 
            'status', 'reg_date'
        )
        
        formatted_results = [
            {
                "Client Id": client['id'],
                "Name": client['name'],
                "Full Name": client['full_name'],
                "Trade Name": client['trade_name'],
                "GST": client['gst'],
                "Code": client['code'],
                "Role": client['role'],
                "Type": client['type'],
                "Email": client['email'],
                "Mobile": client['mobile'],
                "PAN": client['pan'],
                "CIN": client['cin'],
                "Incorporation Date": client['inc_date'],
                "Description": client['description'],
                "File": client['file'],
                # "UID": client['uid'],
                "Status": client['status'],
                "Registration Date": self.make_naive_if_aware(client['reg_date'])
            }
            for client in clients
        ]

        page_size = request.GET.get('pagesize')
        page_no = request.GET.get('page')
        format_type = request.GET.get('type', 'excel').lower()

        if page_size and page_no:
            try:
                page_size = int(page_size)
                page_no = int(page_no)
            except ValueError:
                return Response({'error': 'Invalid pagination parameters'}, status=400)
            start_index = (page_no - 1) * page_size
            end_index = start_index + page_size
            paginated_results = formatted_results[start_index:end_index]
            df = pd.DataFrame(paginated_results)
        else:
            df = pd.DataFrame(formatted_results)
        if format_type == 'csv':
            return self.export_csv(df)
        elif format_type == 'pdf':
            return self.export_pdf(df)
        else:  # Default to Excel
            return self.export_excel(df)
    def make_naive_if_aware(self, dt):
        """Convert a timezone-aware datetime object to a naive datetime."""
        if dt and is_aware(dt):
            return make_naive(dt)
        return dt
    def export_csv(self, df):
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        return FileResponse(csv_buffer, as_attachment=True, filename='exported_client_data.csv', content_type='text/csv')

    def export_excel(self, df):
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        return FileResponse(excel_buffer, as_attachment=True, filename='exported_client_data.xlsx', content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def export_pdf(self, df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)

        # Add table headers
        columns = df.columns
        for column in columns:
            pdf.cell(40, 10, column, 1)
        pdf.ln()

        # Add table rows
        for _, row in df.iterrows():
            for column in columns:
                pdf.cell(40, 10, str(row[column]), 1)
            pdf.ln()

        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        return FileResponse(pdf_buffer, as_attachment=True, filename='exported_client_data.pdf', content_type='application/pdf')


# class ClientExcel(APIView):
#     def post(self, request):
#         if request.method == 'POST' and 'file' in request.FILES:
#             excel_file = request.FILES['file']
#             fs = FileSystemStorage()
#             filename = fs.save(excel_file.name, excel_file)
#             file_path = fs.path(filename)

#             try:
#                 df = pd.read_excel(file_path)

#                 df = df.fillna({
#                     "Name": "",
#                     "FullName": "",
#                     "TradeName": "",
#                     "GST": "",
#                     "Code": "",
#                     "Role": "",
#                     "Type": "",
#                     "Email": "",
#                     "Mobile": "",
#                     "PAN": "",
#                     "CIN": "",
#                     "INCDate": None,
#                     "Description": "",
#                     "File": "",
#                     "UID": None,
#                     "Status": False,
#                     "RegDate": None,
#                 })

#                 client_instances = []
#                 for _, row in df.iterrows():
#                     try:
#                         city = None
#                         if isinstance(row['City'], str):
#                             city = City.objects.get(name=row['City'].capitalize())
#                     except ObjectDoesNotExist:
#                         city = None

#                     try:
#                         state = None
#                         if isinstance(row['State'], str):
#                             state = State.objects.get(name=row['State'].capitalize())
#                     except ObjectDoesNotExist:
#                         state = None

#                     client_instance = UserClient(
#                         name=row['Name'],
#                         full_name=row['FullName'],
#                         trade_name=row['TradeName'],
#                         gst=row['GST'],
#                         code=row['Code'],
#                         role=row['Role'],
#                         type=row['Type'],
#                         email=row['Email'],
#                         mobile=row['Mobile'],
#                         pan=row['PAN'],
#                         cin=row['CIN'],
#                         inc_date=row['INCDate'],
#                         description=row['Description'],
#                         file=row['File'],
#                         uid=row['UID'],
#                         status=row['Status'],
#                         reg_date=datetime.datetime.now()
#                     )
#                     client_instances.append(client_instance)

#                 UserClient.objects.bulk_create(client_instances)
#                 return Response({'message': 'File uploaded and data saved successfully'}, status=200)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=400)
#         return Response({'error': 'Invalid request'}, status=400)

#     def make_naive_if_aware(self, dt):
#         """Convert a timezone-aware datetime object to a naive datetime."""
#         if dt and is_aware(dt):
#             return make_naive(dt)
#         return dt
#     def get(self, request):
#         clients = UserClient.objects.all().values(
#             'id', 'name', 'full_name', 'trade_name', 'gst', 'code', 'role', 'type', 
#             'email', 'mobile', 'pan', 'cin', 'inc_date', 'description', 'file', 'uid', 
#             'status', 'reg_date'
#         )
        
#         formatted_results = [
#             {
#                 "Client Id": client['id'],
#                 "Name": client['name'],
#                 "Full Name": client['full_name'],
#                 "Trade Name": client['trade_name'],
#                 "GST": client['gst'],
#                 "Code": client['code'],
#                 "Role": client['role'],
#                 "Type": client['type'],
#                 "Email": client['email'],
#                 "Mobile": client['mobile'],
#                 "PAN": client['pan'],
#                 "CIN": client['cin'],
#                 "Incorporation Date": client['inc_date'],
#                 "Description": client['description'],
#                 "File": client['file'],
#                 "UID": client['uid'],
#                 "Status": client['status'],
#                 "Registration Date": self.make_naive_if_aware(client['reg_date'])
#             }
#             for client in clients
#         ]
#         page_size = request.GET.get('pagesize')
#         page_no = request.GET.get('page')
#         if page_size and page_no:
#             try:
#                 page_size = int(page_size)
#                 page_no = int(page_no)
#             except ValueError:
#                 return Response({'error': 'Invalid pagination parameters'}, status=400)
#             start_index = (page_no - 1) * page_size
#             end_index = start_index + page_size
#             paginated_results = formatted_results[start_index:end_index]
#             df = pd.DataFrame(paginated_results)
#         else:
#             df = pd.DataFrame(formatted_results)

#         excel_buffer = BytesIO()
#         df.to_excel(excel_buffer, index=False)

#         excel_buffer.seek(0)
#         response = FileResponse(excel_buffer, as_attachment=True, filename='exported_client_data.xlsx')

#         return response
    
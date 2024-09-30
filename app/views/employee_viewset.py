from rest_framework import viewsets,status
from app.serilaizers.employee_serializer import *
from app.serilaizers.login_serializer import UserSerializer
from django.db import transaction
from rest_framework.response import Response
from app.models.user_model import User
from app.serilaizers import extra_serializer

class UserEmployeeViewSet(viewsets.ModelViewSet):
    queryset = UserEmployee.objects.all()
    serializer_class = UserEmployeeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_id = self.request.query_params.get('employee_id')
        employee_name = self.request.query_params.get('employee_name')

        if employee_id:
            try:
                employee_id = int(employee_id)
                queryset = queryset.filter(id=employee_id)
            except ValueError:
                # Handle the case where employee_id is not an integer
                pass
        
        if employee_name:
            queryset = queryset.filter(name=employee_name)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_data = []

        for employee in queryset:
            user = User.objects.filter(id=employee.uid).first()  # Manually fetch the user
            user_serializer = extra_serializer.UserSerializer(user)
            employee_serializer = UserEmployeeSerializer(employee)

            response_data.append({
                "user": user_serializer.data if user else None,  # Handle case if no user is found
                "employee": employee_serializer.data
            })

        return Response(response_data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        employee_data = request.data

        # Validate and create the user
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            with transaction.atomic():
                user = user_serializer.save()

                # Set the uid in the employee data to be the id of the created user
                # employee_data['uid'] = user.id

                # Create the UserEmployee entry
                employee_serializer = UserEmployeeSerializer(data=employee_data)
                if employee_serializer.is_valid():
                    user_employee = employee_serializer.save()

                    # Prepare the response data
                    response_data = {
                        "user": user_serializer.data,
                        "employee": employee_serializer.data
                    }

                    return Response(response_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

import pandas as pd
import datetime
from io import BytesIO
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.utils import timezone

class EmployeeExcel(APIView):

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
                if "Status" not in df.columns:
                    df["Status"] = True
                # Fill missing values with defaults
                df = df.fillna({
                    "FirstName": "",
                    "LastName": "",
                    "Email": "",
                    "Mobile": "",
                    "Username": "",
                    "Password": "",
                    "Password2": "",
                    "Designation": "",
                    "Address": "",
                    "Gender": "",
                    "DOB": pd.NaT,
                    "DOJ": pd.NaT,
                    "AdhaarNumber": "",
                    "PinCode": "",
                    "Status": True,
                })

                employee_instances = []
                with transaction.atomic():
                    for _, row in df.iterrows():
                        # Extract user information from each row
                        dob = row['DOB']
                        doj = row['DOJ']
                        if isinstance(dob, pd.Timestamp):
                            dob = dob.to_pydatetime().date()
                        if isinstance(doj, pd.Timestamp):
                            doj = doj.to_pydatetime().date()
                        user_data = {
                            "first_name": row['FirstName'],
                            "last_name": row['LastName'],
                            "email": row['Email'],
                            "mobile": row['Mobile'],
                            "username": row['Username'],
                            "password": row['Password'],
                            "password2": row['Password2'],
                            "role_id": 3,
                            "status": row['Status'],

                        }
                    
                        user_serializer = UserSerializer(data=user_data)
                        print(user_data)
                        if user_serializer.is_valid():
                            user = user_serializer.save()
                            # Create UserEmployee instance
                            employee_instance = UserEmployee(
                                uid=user.id,  # Link the employee to the created user
                                designation=row['Designation'],
                                address=row['Address'],
                                gender=row['Gender'],
                                dob=dob,
                                doj=doj,
                                adhaar_number=row['AdhaarNumber'],
                                pin_code=row['PinCode']
                            )
                            employee_instances.append(employee_instance)
                        else:
                            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    # Bulk create all the employee instances after users are created
                    UserEmployee.objects.bulk_create(employee_instances)
                    serializer = UserEmployeeSerializer(employee_instances, many=True)

                    return Response({
                        'message': 'File uploaded and data saved successfully',
                        'employees': serializer.data
                    }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        employees = UserEmployee.objects.all().values(
            'id', 'uid', 'designation', 'address', 'gender', 'dob', 'doj', 
            'adhaar_number', 'pin_code'
        )
        
        formatted_results = [
            {
                "Employee ID": employee['id'],
                "UID": employee['uid'],
                "Designation": employee['designation'],
                "Address": employee['address'],
                "Gender": employee['gender'],
                "Date of Birth": employee['dob'],
                "Date of Joining": employee['doj'],
                "Adhaar Number": employee['adhaar_number'],
                "Pin Code": employee['pin_code'],
            }
            for employee in employees
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

    def export_csv(self, df):
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        return FileResponse(csv_buffer, as_attachment=True, filename='exported_employee_data.csv', content_type='text/csv')

    def export_excel(self, df):
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        return FileResponse(excel_buffer, as_attachment=True, filename='exported_employee_data.xlsx', content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def export_pdf(self, df):
        from fpdf import FPDF
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
        return FileResponse(pdf_buffer, as_attachment=True, filename='exported_employee_data.pdf', content_type='application/pdf')
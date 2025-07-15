from django.shortcuts import  get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from .models import CustomUser, Department, Designation, Employee,EmployeeCurrentAddress, EmployeePermanentAddress, EmployeeDocuments, EmployeeBankDetails, Leads, Client, Team, Meeting
from .serializers import UserSerializer, DepartmentSerializer, DesignationSerializer, EmployeeSerializer,EmployeeCurrentAddressSerializer, EmployeePermanentAddressSerializer, EmployeeDocumentsSerializer, EmployeeBankDetailsSerializer, EmployeesNameSerializer, LeadsNameSerializer, ClientsNameSerializer, TeamSerializer, ClientSerializer, LeadsSerializer, MeetingSerializer, EmployeeGetAPISerializer

from django.db import transaction
from app.pagination import CustomPagination
# Create your views here.

# User login view
class UserLoginView(APIView):
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = CustomUser.objects.filter(email=email).first()
        
        if not user:
            return Response({"error": "Email is not registered."}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({"error": "User is not active. Please contact to super admin."}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(request= request, email=email, password=password)
        
        if user:
            refreshToken = RefreshToken.for_user(user)
            return Response({
                "refreshToken" : str(refreshToken),
                "accesToken": str(refreshToken.access_token),
                "user_type": user.user_type
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Password is not valid"}, status=status.HTTP_401_UNAUTHORIZED)
    
# User registeration view
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# View of department
class DepartmentView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all().order_by('-updated_at')
    serializer_class = DepartmentSerializer

# View of designation
class DesignationView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset  = Designation.objects.all().order_by("-updated_at")
    serializer_class = DesignationSerializer

class EmployeeGetAPI(APIView):
    def get(self, request):
        employee_data = Employee.objects.all()
        ser_res = EmployeeGetAPISerializer(employee_data, many = True)
        return Response(ser_res.data, status=status.HTTP_200_OK)

class EmployeeView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Employee.objects.all().order_by('-updated_at')
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'designation']
    search_fields = ['name', 'user__email', 'contact_no']
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    


    def update(self, request, pk, *args, **kwargs):
        try:
            employee = get_object_or_404( Employee, pk= pk)
            data = request.data

            # Get the related user data
            user = employee.user
        
            
            current_address_data = {
                
                "address" : data.get("current_address.address"),
                "city" : data.get("current_address.city"),
                "state" : data.get("current_address.state"),
                "pincode" : data.get("current_address.pincode"),
                "country" : data.get("current_address.country"),
            }
            permanent_address_data = {
                "address" : data.get("permanent_address.address"),
                "city" : data.get("permanent_address.city"),
                "state" : data.get("permanent_address.state"),
                "pincode" : data.get("permanent_address.pincode"),
                "country" : data.get("permanent_address.country"),
            }

            documents_data = {
                "higher_education_certificate" : data.get("documents.higher_education_certificate", employee.documents.higher_education_certificate),
                "resume" : data.get("documents.resume", employee.documents.resume),
                "aadhar_card" : data.get("documents.aadhar_card", employee.documents.aadhar_card),
                "pan_card" : data.get("documents.pan_card", employee.documents.pan_card),
                "photo" : data.get("documents.photo", employee.documents.photo),
            }
            bank_details_data = {
                "account_holder_name": data.get("bank_details.account_holder_name" , employee.bank_details.account_holder_name), 
                "bank_name": data.get("bank_details.bank_name" , employee.bank_details.bank_name), 
                "account_number": data.get("bank_details.account_number" , employee.bank_details.account_number), 
                "ifsc_code": data.get("bank_details.ifsc_code" , employee.bank_details.ifsc_code), 
                "branch": data.get("bank_details.branch" , employee.bank_details.branch), 
            }

            
            # Checking if email is already present or not
            if data.get('user.email') != user.email and CustomUser.objects.filter(email=data.get('user.email')).exclude(pk=user.pk).exists():
                    return Response({"error": "This email is already taken."}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                
                # Updating the user fields
                user.email = data.get('user.email', user.email)
                user.user_type = data.get("user.user_type", user.user_type)
                user.is_active = data.get("user.is_active", user.is_active)
                if (user.is_active == "true"):
                    user.is_active = True
                elif (user.is_active == "false"):
                    user.is_active = False
                password = data.get("user.password")
                confirm_password = data.get("user.confirm_password")
                
                if (password and confirm_password):
                    if  (password == confirm_password):
                        user.set_password(password)
                    else:
                        return Response({"error": "Password and confirm password did not match."}, status=status.HTTP_400_BAD_REQUEST)
                user.save()

                # Updating the employee fields
                employee.name = data.get("name", employee.name)
                employee.father_name = data.get('father_name', employee.father_name)
                employee.contact_no = data.get("contact_no", employee.contact_no)
                employee.alternate_contact_no = data.get("alternate_contact_no", employee.alternate_contact_no)
                employee.gender = data.get("gender", employee.gender)
                employee.joining_date = data.get("joining_date", employee.joining_date)
                
                employee.aadhar_no = data.get('aadhar_no', employee.aadhar_no)
                employee.pan_no = data.get('pan_no', employee.pan_no)
                employee.basic_salary = data.get('basic_salary', employee.basic_salary)
                if data.get('dob'):
                    employee.dob = data.get('dob')
                
                employee.department = Department.objects.get(id=data.get('department_id', employee.department)) 
                employee.designation = Designation.objects.get(id = data.get('designation_id', employee.designation) ) 
                employee.save()

            
            
                if current_address_data:
                    if hasattr(employee, 'current_address'):
                        
                        current_address_ser = EmployeeCurrentAddressSerializer(employee.current_address, data = current_address_data, partial = True)
                        if current_address_ser.is_valid():
                            current_address_ser.save()
                    else:
                        EmployeeCurrentAddress.objects.create(employee = employee, **current_address_data)

                if permanent_address_data:
                    if hasattr(employee, 'permanent_address'):
                        permanent_address_ser = EmployeePermanentAddressSerializer(employee.permanent_address, data = permanent_address_data, partial = True)
                        if permanent_address_ser.is_valid():
                            permanent_address_ser.save()
                    else:
                        EmployeeCurrentAddress.objects.create(employee = employee, **permanent_address_data)

                if documents_data:
                    if hasattr(employee, 'documents'):
                        documents_ser = EmployeeDocumentsSerializer(employee.documents, data = documents_data, partial = True)
                        if documents_ser.is_valid():
                            documents_ser.save()

                    else:
                        EmployeeDocuments.objects.create(employee = employee, **documents_data)

                if bank_details_data:
                    if hasattr(employee, 'bank_details'):
                        bank_details_ser = EmployeeBankDetailsSerializer(employee.bank_details, data = bank_details_data, partial = True)
                        if bank_details_ser.is_valid():
                            bank_details_ser.save()

                    else: 
                        EmployeeBankDetails.objects.create(employee = employee, **bank_details_data)
                    
            
            return Response({"detail": "Employee data updated successfully."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
     # To delete the user and employee
    
    
    def destroy(self, request,pk, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=pk)
        user = CustomUser.objects.filter(id = employee.user.id)
        
        with transaction.atomic():
            employee.delete()
            user.delete()  # manually delete linked user
        return Response({"detail": "Employee and user deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# To get employees name only
class EmployeeNameView(APIView):
    def get(self, request):
        employee_name_data = Employee.objects.all().values('id', 'name')
        ser_res = EmployeesNameSerializer(employee_name_data, many = True)
        return Response(ser_res.data, status=status.HTTP_200_OK)
    

# To get leads name only
class LeadNameView(APIView):
    def get(self, request):
        lead_name_data = Leads.objects.all().values('id', 'name')
        ser_res = LeadsNameSerializer(lead_name_data, many = True)
        return Response(ser_res.data, status=status.HTTP_200_OK)
    

# To get clients name only
class ClientNameView(APIView):
    def get(self, request):
        client_name_data = Client.objects.all().values('id', 'name')
        ser_res = ClientsNameSerializer(client_name_data, many = True)
        return Response(ser_res.data, status=status.HTTP_200_OK)
    
# Team View
class TeamView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class=CustomPagination
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    ordering = ['-updated_at']
    

    
# Client View
class ClientView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Client.objects.all().order_by('-updated_at')
    serializer_class = ClientSerializer

    def update(self, request, pk, *args, **kwargs):
        try:
            client = get_object_or_404( Client, pk= pk)
            data = request.data

            # Get the related user data
            user = client.user
            
            
            # Checking if email is already present or not
            if data.get('user.email') != user.email and CustomUser.objects.filter(email=data.get('user.email')).exclude(pk=user.pk).exists():
                    return Response({"error": "This email is already taken."}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                
                # Updating the user fields
                user.email = data.get('user.email', user.email)
                user.user_type = data.get("user.user_type", user.user_type)
                user.is_active = data.get("user.is_active", user.is_active)
                if (user.is_active == "true"):
                    user.is_active = True
                elif (user.is_active == "false"):
                    user.is_active = False
                password = data.get("user.password")
                confirm_password = data.get("user.confirm_password")
                
                if (password and confirm_password):
                    if  (password == confirm_password):
                        user.set_password(password)
                    else:
                        return Response({"error": "Password and confirm password did not match."}, status=status.HTTP_400_BAD_REQUEST)
                user.save()

                # Updating the employee fields
                client.name = data.get("name", client.name)
                client.phone = data.get("phone", client.phone)
                client.gender = data.get("gender", client.gender)
                client.address = data.get("address", client.address)
                client.country = data.get("country", client.country)
                client.state = data.get("state", client.state)
                client.pincode = data.get("pincode", client.pincode)

                client.save()
                    
            
            return Response({"detail": "Employee data updated successfully."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
     # To delete the user and employee
    

#meeting
class MeetingView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Meeting.objects.all().order_by('-updated_at')
    serializer_class = MeetingSerializer

    def create(self, request, *args, **kwargs):

       try:
            if request.user.user_type  == CustomUser.EMPLOYEE or request.user.is_superuser: 
                request.data['scheduled_by_id'] = request.user.id
                return super().create(request, *args, **kwargs)
            return Response( {"error": "User is not an employee."},status=status.HTTP_400_BAD_REQUEST)
       except Exception as e:
           return Response( {"error": str(e)},status=status.HTTP_400_BAD_REQUEST)

#leads
class LeadsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Leads.objects.all().order_by('-updated_at')
    serializer_class = LeadsSerializer

    

    
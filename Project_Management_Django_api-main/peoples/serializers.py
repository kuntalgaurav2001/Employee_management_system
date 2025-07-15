from rest_framework import serializers
from .models import CustomUser, Department, Designation, EmployeeDocuments, EmployeeBankDetails, Employee, EmployeeCurrentAddress, EmployeePermanentAddress,  Client, Leads, Team, Meeting
from django.db import transaction

# Custom User serializer
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','email','password','confirm_password', 'is_active','user_type']
        read_only_fields = ['created_at', 'updated_at']
        # exclude = ['is_superuser', 'is_staff', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        
        if not attrs.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "This field is required."})
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"error": "Password and confirm password doesn't match. "})
        value = attrs.pop('confirm_password')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
# Serializer of department
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

# Serilizer of designation
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = "__all__"

# Serializer for Employee Address
# class EmployeeAddressSerilizer(serializers.ModelSerializer):

    # class Meta:
    #     model = EmployeeAddress
    #     fields = "__all__"
    #     extra_kwargs = {"employee": {"required": False}}

class EmployeeCurrentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCurrentAddress
        fields = "__all__"
        extra_kwargs = {"employee": {"required": False}}

class EmployeePermanentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePermanentAddress
        fields = "__all__"
        extra_kwargs = {"employee": {"required": False}}

# Serializer for Employee Documents
class EmployeeDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDocuments
        fields = "__all__"
        extra_kwargs = {"employee": {"required": False}}

# Serializer for Employee bank details
class EmployeeBankDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeBankDetails
        fields = "__all__"
        extra_kwargs = {"employee": {"required": False}}


# Serializer of employee
class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department_id = serializers.PrimaryKeyRelatedField(
        source='department', queryset=Department.objects.all(), write_only=True
    )
    designation_id = serializers.PrimaryKeyRelatedField(
        source='designation', queryset=Designation.objects.all(), write_only=True
    )
    department = DepartmentSerializer(read_only = True)
    designation = DesignationSerializer(read_only = True)
    
    current_address = EmployeeCurrentAddressSerializer()
    permanent_address = EmployeePermanentAddressSerializer()
    documents = EmployeeDocumentsSerializer()
    bank_details = EmployeeBankDetailsSerializer()
    class Meta:
        model = Employee
        fields = "__all__"

    

    def create(self, validated_data):
        
        user_data = validated_data.pop('user', {})
        # addresses_data = validated_data.pop('addresses', [])
        current_address_data = validated_data.pop('current_address', {})
        permanent_address_data = validated_data.pop('permanent_address', {})
        documents_data = validated_data.pop('documents', {})
        bank_details_data = validated_data.pop('bank_details', {})

        with transaction.atomic():
            # Creates user
            user = CustomUser.objects.create_user(**user_data)
            # creates employee
            employee = Employee.objects.create(user = user, **validated_data)
            
            # creates employee address
            # if addresses_data:
            # for address_data in addresses_data:
            #    EmployeeAddress.objects.create(employee = employee, **address_data)

            EmployeeCurrentAddress.objects.create(employee = employee, **current_address_data)
            EmployeePermanentAddress.objects.create(employee = employee, **permanent_address_data)
            
            # Creates employee documents
            # if documents_data:
            EmployeeDocuments.objects.create(employee = employee, **documents_data)

            # create employee's bank details 
            # if bank_details_data:
            EmployeeBankDetails.objects.create(employee = employee, **bank_details_data)

            return employee
    

# To get employee name only
class EmployeesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name']


# To get Lead name only
class LeadsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = ['id', 'name']

# To get Client name only
class ClientsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']

# Team Serializer
class TeamSerializer(serializers.ModelSerializer):
    
    team_lead = EmployeesNameSerializer(read_only =True)
    team_members = EmployeesNameSerializer(read_only = True, many = True)
    team_lead_id = serializers.PrimaryKeyRelatedField(
        source = 'team_lead', queryset = Employee.objects.all(), write_only=True
    )
    team_members_id = serializers.PrimaryKeyRelatedField(
        source = 'team_members', queryset = Employee.objects.all(), write_only = True, many = True
    )
    class Meta:
        model = Team
        fields = "__all__"

    def validate(self, attrs):
        team_lead = attrs.get('team_lead')
        team_members = attrs.get('team_members',[])
        
        all_employees = list(team_members)
       
        if team_lead in team_members:
            raise serializers.ValidationError(f"{team_lead} cannot be a team member.")
        
        if team_lead:
            all_employees.append(team_lead)
        

        # Check if any of them is already assigned to a team (as lead or member)
        for emp in all_employees:
            if Team.objects.filter(team_lead=emp).exclude(id=self.instance.id if self.instance else None).exists():
                raise serializers.ValidationError(f"{emp.name} is already a team lead in another team.")
            if Team.objects.filter(team_members=emp).exclude(id=self.instance.id if self.instance else None).exists():
                raise serializers.ValidationError(f"{emp.name} is already a team member in another team.")
        
        return attrs

# Meeting serializer
class MeetingSerializer(serializers.ModelSerializer):
    scheduled_by=serializers.SerializerMethodField()
    scheduled_by_id = serializers.PrimaryKeyRelatedField(
        source = 'scheduled_by', queryset = CustomUser.objects.all(), write_only = True, required = False
    )
    meeting_members = EmployeesNameSerializer(read_only = True, many = True)
    meeting_members_id = serializers.PrimaryKeyRelatedField(
        source = 'meeting_members', queryset = Employee.objects.all(), write_only = True, many=True
    )
    class Meta:
        model = Meeting
        fields = "__all__"

    def get_scheduled_by(self, obj):
        try:
            return obj.scheduled_by.employee.name  # assuming CustomUser has related_name="employee"
        except AttributeError:
            return None

#leads serializer
class LeadsSerializer(serializers.ModelSerializer):
    assign_to=EmployeesNameSerializer(read_only=True)
    assign_to_id = serializers.PrimaryKeyRelatedField(
        source = 'assign_to', queryset = Employee.objects.all(), write_only = True
    )
    class Meta:
        model = Leads
        fields = "__all__"

#Client serializer
class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Client
        fields = "__all__"
    
    def validate(self, attrs):
        if not attrs.get('user').get('user_type'):
            attrs['user']['user_type'] = "Client"
        return super().validate(attrs)

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        
        with transaction.atomic():
            user = CustomUser.objects.create_user(**user_data)
            client = Client.objects.create(user = user, **validated_data )
            return client
    

class EmployeeGetAPISerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    department = DepartmentSerializer(read_only = True)
    designation = DesignationSerializer(read_only = True)
    
    current_address = EmployeeCurrentAddressSerializer(read_only = True)
    permanent_address = EmployeePermanentAddressSerializer(read_only = True)
    documents = EmployeeDocumentsSerializer(read_only = True)
    bank_details = EmployeeBankDetailsSerializer(read_only = True)
    class Meta:
        model = Employee
        fields = "__all__"
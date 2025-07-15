from rest_framework import serializers
from peoples.serializers import LeadsNameSerializer, EmployeesNameSerializer, ClientsNameSerializer
from peoples.models import Leads, Employee, Client
from .models import  *



# To get Project name only
class ProjectsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title']


#Proposal serializer
class ProposalsSerializer(serializers.ModelSerializer):
    lead_name=serializers.StringRelatedField(read_only=True)
    lead_name_id = serializers.PrimaryKeyRelatedField(
        source = 'lead_name', queryset = Leads.objects.all(), write_only = True
    )
    class Meta:
        model = Proposals
        fields = "__all__"


# Contracts serializer
class ContractsSerializer(serializers.ModelSerializer):
    lead_name=LeadsNameSerializer(read_only=True)
    lead_name_id= serializers.PrimaryKeyRelatedField(
        source = 'lead_name', queryset = Leads.objects.all(), write_only = True
    )
    class Meta:
        model = Contracts
        fields = "__all__"


# Project serializer
class ProjectSerializer(serializers.ModelSerializer):
    assigned_to=EmployeesNameSerializer(read_only=True)
    client_name=ClientsNameSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        source = 'assigned_to', queryset = Employee.objects.all(), write_only = True
    )
    client_name_id = serializers.PrimaryKeyRelatedField(
        source = 'client_name', queryset = Client.objects.all(), write_only = True
    )
    
    class Meta:
        model = Project
        fields = "__all__"

#Task serializer
class TaskSerializer(serializers.ModelSerializer):
    project_name=ProjectsNameSerializer(read_only=True)
    assign_to=EmployeesNameSerializer(read_only=True)
    project_name_id = serializers.PrimaryKeyRelatedField(
        source = 'project_name', queryset = Project.objects.all(), write_only = True
    )
    assign_to_id = serializers.PrimaryKeyRelatedField(
        source = 'assign_to', queryset = Employee.objects.all(), write_only = True
    )

    class Meta:
        model = Task
        fields = "__all__"


# Todo serializer
class ToDoSerializer(serializers.ModelSerializer):
    created_by=EmployeesNameSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        source = 'created_by', queryset = Employee.objects.all(), write_only = True
    )
    class Meta:
        model = ToDo
        fields = "__all__"

#Tickets serializer
class TicketsSerializer(serializers.ModelSerializer):
    project_name = ProjectsNameSerializer(read_only = True)
    client_name = ClientsNameSerializer(read_only = True)
    assign_to = EmployeesNameSerializer(read_only = True)
    project_name_id = serializers.PrimaryKeyRelatedField(
        source = 'project_name', queryset = Project.objects.all(), write_only = True
    )
    client_name_id = serializers.PrimaryKeyRelatedField(
        source = 'client_name', queryset = Client.objects.all(), write_only = True
    )
    assign_to_id = serializers.PrimaryKeyRelatedField(
        source = 'assign_to', queryset = Employee.objects.all(), write_only = True
    )
    class Meta:
        model = Tickets
        fields = "__all__"

#announcement serializer
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"
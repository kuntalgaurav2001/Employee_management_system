from django.shortcuts import  get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import  Project, Proposals, Contracts, Task, ToDo, Tickets, Announcement
from .serializers import  ProjectsNameSerializer, ProposalsSerializer, ContractsSerializer, ProjectSerializer, TaskSerializer, ToDoSerializer, TicketsSerializer, AnnouncementSerializer
from .pagination import CustomPagination


# Create your views here.


# To get Project name only
class ProjectNameView(APIView):
    def get(self,request):
        project_name_data = Project.objects.all().values('id', 'title')
        ser_res = ProjectsNameSerializer(project_name_data, many = True)
        return Response(ser_res.data, status=status.HTTP_200_OK)

# Proposals View
class ProposalsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Proposals.objects.all().order_by('-updated_at')
    serializer_class = ProposalsSerializer
    
# Contracts view
class ContractsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Contracts.objects.all().order_by('-updated_at')
    serializer_class = ContractsSerializer

# Project View
class ProjectView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Project.objects.all().order_by('-updated_at')
    serializer_class = ProjectSerializer

# Task View
class TaskView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Task.objects.all().order_by('-updated_at')
    serializer_class = TaskSerializer

# Todo View
class ToDoView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = ToDo.objects.all().order_by('-updated_at')
    serializer_class = ToDoSerializer

#tickets
class TicketsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class=CustomPagination
    queryset = Tickets.objects.all().order_by('-updated_at')
    serializer_class = TicketsSerializer

#announcement
class AnnouncementView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Announcement.objects.all().order_by('-updated_at')
    serializer_class = AnnouncementSerializer

from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProjectNameView, ProposalsView, ContractsView, ProjectView, TaskView, ToDoView, TicketsView, AnnouncementView

router = DefaultRouter()
router.register(r'proposals',ProposalsView )
router.register(r'contracts',ContractsView )
router.register(r'project',ProjectView )
router.register(r'task',TaskView )
router.register(r'todo',ToDoView )
router.register(r'tickets',TicketsView )
router.register(r'announcement',AnnouncementView )

urlpatterns = [
    path('', include(router.urls)),
    path('projects-name/', ProjectNameView.as_view()),
]
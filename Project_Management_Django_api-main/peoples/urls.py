
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeView, DepartmentView, DesignationView, TeamView, UserLoginView, UserRegisterView, EmployeeNameView, LeadNameView, ClientNameView, MeetingView, LeadsView, EmployeeGetAPI, ClientView

router = DefaultRouter()
router.register(r'employee',EmployeeView )
router.register(r'departments',DepartmentView )
router.register(r'designations',DesignationView )
router.register(r'teams',TeamView )
router.register(r'meetings',MeetingView )
router.register(r'leads',LeadsView )
router.register(r'clients',ClientView )


urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginView.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('employees-name/', EmployeeNameView.as_view()),
    path('leads-name/', LeadNameView.as_view()),
    path('clients-name/', ClientNameView.as_view()),
    path("employee-get-data/", EmployeeGetAPI.as_view()),
]
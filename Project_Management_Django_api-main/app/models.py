from django.db import models
import uuid
from .base import BaseModel
from peoples.models import Leads, Employee, Client
from .validators import email_validator, password_validator, contact_no_validator, aadhar_no_validator
# Create your models here.




class Proposals(BaseModel):
    DISCUSSING = "Discussing"
    ACCEPT = "Accept"
    REJECT = "Reject"
    STATUS_CHOICES = [(DISCUSSING, "Discussing"),
                      (ACCEPT , "Accept"),
                      (REJECT , "Reject")]
    lead_name = models.ForeignKey(Leads, on_delete=models.CASCADE, related_name="lead_name")
    title = models.CharField(max_length=250)
    value = models.BigIntegerField()
    date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

class Contracts(BaseModel):
    PENDING = "Pending"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACTIVE, "Active"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled")
    ]
    name = models.CharField(max_length=250)
    lead_name = models.ForeignKey(Leads, on_delete=models.CASCADE, related_name="lead")
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.BigIntegerField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    description = models.TextField()



class Project(BaseModel):
    
    NOT_STARTTED= "Not Started"
    PLANNING = "Planning"
    IN_PROGRESS = "In Progress"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    STATUS_CHOICES = [
        (NOT_STARTTED, "Not Started"),
        (PLANNING, "Planning"),
        (IN_PROGRESS, "In Progress"),
        (PAUSED, "Paused"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled")
    ]
    title = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL,null=True, related_name="project_assigned_to")
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="project_client")
    budget = models.BigIntegerField()
    description = models.TextField()


    
class Task(BaseModel):

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    PRIORITY_CHOICES = [
        (HIGH,"High"),
        (MEDIUM,"Medium"),
        (LOW,"Low")
    ]

    TODO ="ToDo"
    IN_PROGRESS ="In Progress"
    DONE ="Done"
    STATUS_CHOICES = [
        (TODO,"ToDo"),
        (IN_PROGRESS,"In Progress"),
        (DONE,"Done")
    ]


    task_name = models.CharField(max_length=250)
    project_name = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="project_name")
    assign_to = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,related_name="task_assign_to")
    priority = models.CharField(max_length=15,choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15,choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    



class ToDo(BaseModel):

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    PRIORITY_CHOICES = [
        (HIGH,"High"),
        (MEDIUM,"Medium"),
        (LOW,"Low")
    ]

    TODO ="ToDo"
    IN_PROGRESS ="In Progress"
    DONE ="Done"
    STATUS_CHOICES = [
        (TODO,"ToDo"),
        (IN_PROGRESS,"In Progress"),
        (DONE,"Done")
    ]

    created_by = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,related_name="created_by")
    todo_name = models.CharField(max_length=20)
    priority = models.CharField(max_length=15,choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15,choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()



class Tickets(BaseModel):

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    PRIORITY_CHOICES = [
        (HIGH,"High"),
        (MEDIUM,"Medium"),
        (LOW,"Low")
    ]

    OPEN = "Open"
    CLOSE = "Close"
    STATUS_CHOICES = [
        (OPEN,"Open"),
        (CLOSE,"Close")
    ]

    title = models.CharField(max_length=250)
    description = models.TextField()
    project_name = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="tickets_project_name")
    client_name = models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,related_name="tickets_client_name")
    assign_to = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,related_name="tickets_assign_to")
    priority = models.CharField(max_length=15,choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15,choices=STATUS_CHOICES)


class Announcement(BaseModel):

    CLIENT = "Client"
    EMPLOYEE = "Employee"
    BOTH = "Both"
    WHOM_TO_SEND_CHOICES =[
        (CLIENT,"Client"),
        (EMPLOYEE,"Employee"),
        (BOTH,"Both")
    ]
    subject = models.CharField(max_length=250)
    description = models.TextField()
    whom_to_send = models.CharField(max_length=15,choices = WHOM_TO_SEND_CHOICES)
    date = models.DateField()





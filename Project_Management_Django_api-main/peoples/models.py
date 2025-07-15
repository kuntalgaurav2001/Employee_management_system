from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from app.base import BaseModel
from app.validators import email_validator, password_validator, contact_no_validator, aadhar_no_validator
from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage
from cloudinary.models import CloudinaryField
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    EMPLOYEE = "Employee"
    CLIENT = "Client"
    USER_TYPE_CHOICES = [
        ( EMPLOYEE, 'Employee'),
        (CLIENT, 'Client'),
    ]

    email = models.EmailField(unique=True, validators=[email_validator])
    # password = models.CharField(_("password"), max_length=128, validators=[password_validator])
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    username = None  # Remove username field since we use email for login

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_type"]

    def __str__(self):
        return f"{self.email} - {self.user_type}"
    


# Department of employee
class Department(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

# Designation of employee
class Designation(BaseModel):
    title = models.CharField(max_length=100)
    level = models.IntegerField(default=0)  


# Employee's personal details
class Employee(BaseModel):

    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="employee")
    employee_id = models.CharField(max_length=15, unique=True, blank=True)
    name = models.CharField(max_length = 250)
    father_name = models.CharField(max_length=250)
    contact_no = models.CharField(max_length=250, validators=[contact_no_validator])
    alternate_contact_no = models.CharField(max_length=15, validators=[contact_no_validator], null=True, blank=True)
    gender = models.CharField(max_length=10, choices= GENDER_CHOICES, default=MALE)
    pan_no = models.CharField(max_length=20)
    aadhar_no = models.CharField(max_length=12, validators=[aadhar_no_validator])
    dob = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name="department_employees", null=True)
    designation = models.ForeignKey(Designation, on_delete= models.SET_NULL, related_name="designation_employees", null=True)
    joining_date = models.DateField()
    # role = models.ForeignKey()
    basic_salary = models.IntegerField()
    
    def save(self, *args, **kwargs) :
        if not self.employee_id:
            last_emp = Employee.objects.order_by('created_at').last()
            if last_emp and last_emp.employee_id:
                last_id = int(last_emp.employee_id.replace("EMP", ""))
            else:
                last_id = 0
            new_id = f"EMP{last_id + 1:03d}"  
            self.employee_id = new_id
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# Employee's addresses  
# class EmployeeAddress(BaseModel):
#     CURRENT = "Current"
#     PERMANENT = "Permanent"
#     ADDRESS_CHOICE = [
#         (CURRENT , "Current"),
#         (PERMANENT, "Permanent"),
#     ]
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='addresses')
#     address_type = models.CharField(max_length=10, choices=ADDRESS_CHOICE)
#     address_line = models.TextField()
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     pincode = models.IntegerField()
#     country = models.CharField(max_length=100, default="India")

class EmployeeCurrentAddress(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='current_address')
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    country = models.CharField(max_length=100)

class EmployeePermanentAddress(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='permanent_address')
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    country = models.CharField(max_length=100)

# Employee's documents
class EmployeeDocuments(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="documents")
    # higher_education_certificate = models.FileField(upload_to='employee/documents/higher_education_certificate/', null=True, blank=True)
    # resume = models.FileField(upload_to='employee/documents/resume/', null=True, blank=True)
    # aadhar_card = models.FileField(upload_to='employee/documents/aadhar_card/', null=True, blank=True)
    # pan_card = models.FileField(upload_to='employee/documents/pan_card/', null=True, blank=True)
    # photo = models.FileField(upload_to='employee/documents/photo/', null=True, blank=True)
    higher_education_certificate = models.FileField(
        storage=RawMediaCloudinaryStorage(),
        upload_to='employee/documents/higher_education_certificate/',
        null=True, blank=True
    )
    resume = models.FileField(
        storage=RawMediaCloudinaryStorage(),
        upload_to='employee/documents/resume/',
        null=True, blank=True
    )
    aadhar_card = models.FileField(
        storage=RawMediaCloudinaryStorage(),
        upload_to='employee/documents/aadhar_card/',
        null=True, blank=True
    )
    pan_card = models.FileField(
        storage=RawMediaCloudinaryStorage(),
        upload_to='employee/documents/pan_card/',
        null=True, blank=True
    )
    photo = models.ImageField(storage=MediaCloudinaryStorage() , upload_to='employee/documents/photo/', null=True, blank=True)

# Employee's bank details 
class EmployeeBankDetails(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="bank_details")
    account_holder_name = models.CharField(max_length=250)
    bank_name = models.CharField(max_length=250)
    account_number = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=100)
    branch = models.CharField(max_length=150)

# Team details
class Team(BaseModel):
    name = models.CharField(max_length=250)
    team_lead = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name = "team_lead")
    team_members = models.ManyToManyField(Employee, related_name="team_members")
    note = models.TextField(null=True, blank=True)

# Meeting details
class Meeting(BaseModel):
    
    SCHEDULED = "Scheduled"
    RESCHEDULED = "Rescheduled"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    STATUS_CHOICES= [
        (SCHEDULED,"Scheduled"),
        (RESCHEDULED, "Rescheduled"),
        (CANCELLED, "Cancelled"),
        (COMPLETED, "Completed")
    ]
    name = models.CharField(max_length=250)
    agenda = models.TextField()
    start_date_and_time = models.DateTimeField()
    meeting_members = models.ManyToManyField(Employee, related_name='meeting_members')
    meeting_link = models.URLField()
    duration = models.CharField(max_length=10)
    scheduled_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="scheduled_by", null=True)
    status = models.CharField(max_length=20)


# Leads details
class Leads(BaseModel):
    NEW = "New"
    DISCUSSION = "Discussion"
    WON = "Won"
    LOST = "Lost"
    STATUS_CHOICES = [
        (NEW, "New"),
        (DISCUSSION, "Discussion"),
        (WON, "Won"),
        (LOST, "Lost"),
    ]
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    lead_source = models.CharField(max_length=100)
    description = models.TextField()
    assign_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="assign_to")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

# Client details
class Client(BaseModel):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    GENDER_CHOICES = [
        (MALE,"Male"),
        (FEMALE, "Female"),
        (OTHER,"Other"),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="client_user")
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
from django.db import models
from app.base import BaseModel
from app.models import  Project
from app.validators import only_numbers_allowed, contact_no_validator
from peoples.models import Client, Employee
# Create your models here.



class BankAccounts(BaseModel):

    SAVINGS = "Savings"
    CURRENT ="Current"
    ACCOUNT_TYPE_CHOICES = [
        (SAVINGS,"Savings"),
        (CURRENT,"Current")
    ]


    OPEN = "Open"
    CLOSE = "Close"
    STATUS_CHOICES = [
        (OPEN,"Open"),
        (CLOSE,"Close")
    ]

    bank_name =models.CharField(max_length=250)
    account_holder_name = models.CharField(max_length=250)
    account_number = models.CharField(max_length=15, validators=[only_numbers_allowed])
    account_type = models.CharField(max_length=20,choices=ACCOUNT_TYPE_CHOICES)
    contact_number = models.CharField(max_length=15, validators=[contact_no_validator])
    branch = models.CharField(max_length=250)
    ifsc_code = models.CharField(max_length=250)
    status = models.CharField(max_length=15,choices=STATUS_CHOICES)

    

class Invoices(BaseModel):
    PAID = "Paid"
    DUE = "Due"
    OVERDUE = "Overdue"
    STATUS_CHOICES = [
        (PAID,"Paid"),
        (DUE,"Due"),
        (OVERDUE,"Overdue")
    ]

    UPI = "upi"
    CREDIT_CARD ="Credit Card"
    DEBIT_CARD ="Debit Card"
    CASH = "Cash"
    OTHERS ="Others"
    PAYMENT_METHOD_CHOICES = [
        (UPI,"upi"),
        (CREDIT_CARD,"Credit Card"),
        (DEBIT_CARD,"Debit Card"),
        (CASH,"Cash"),
        (OTHERS,"Others")
    ]

    invoice_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=15,choices=STATUS_CHOICES)
    project_name = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="invoices_project_name")
    client_name = models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,related_name="invoices_client_name")
    subtotal = models.BigIntegerField()
    discount = models.IntegerField()
    gst = models.IntegerField()
    cgst = models.IntegerField()
    vat = models.IntegerField()
    other_tax = models.IntegerField()
    total = models.BigIntegerField()
    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES)
    payment_id = models.CharField(max_length=250)
    bank_account = models.ForeignKey(BankAccounts,on_delete=models.SET_NULL,null=True,related_name="invoices_bank_account")
    note = models.TextField()
    generated_by = models.CharField(max_length=250)

class Income(BaseModel):
    UPI = "upi"
    CREDIT_CARD ="Credit Card"
    DEBIT_CARD ="Debit Card"
    CASH = "Cash"
    OTHERS ="Others"
    PAYMENT_MODE_CHOICES = [
        (UPI,"upi"),
        (CREDIT_CARD,"Credit Card"),
        (DEBIT_CARD,"Debit Card"),
        (CASH,"Cash"),
        (OTHERS,"Others")
    ]

    client_name = models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,related_name="income_client_name")
    project_name = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="income_project_name")
    amount = models.BigIntegerField()
    payment_mode = models.CharField(max_length=20,choices=PAYMENT_MODE_CHOICES)
    payment_id = models.CharField(max_length=250) 
    income_date = models.DateField()  
    bank_account = models.ForeignKey(BankAccounts,on_delete=models.SET_NULL,null=True,related_name="income_bank_account")


class Expenses(BaseModel):

    UPI = "upi"
    CREDIT_CARD ="Credit Card"
    DEBIT_CARD ="Debit Card"
    CASH = "Cash"
    OTHERS ="Others"
    PAYMENT_MODE_CHOICES = [
        (UPI,"upi"),
        (CREDIT_CARD,"Credit Card"),
        (DEBIT_CARD,"Debit Card"),
        (CASH,"Cash"),
        (OTHERS,"Others")
    ]
    name = models.CharField(max_length=250)
    amount = models.IntegerField()
    date = models.DateField()
    purchased_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null = True, related_name="purchased_by")
    purchased_from = models.CharField(max_length=100)
    bank_account = models.ForeignKey(BankAccounts, on_delete=models.SET_NULL, null=True, related_name="expenses_bank_account")
    payment_mode = models.CharField(max_length=20,choices=PAYMENT_MODE_CHOICES)
    payment_id = models.CharField(max_length=250)
    

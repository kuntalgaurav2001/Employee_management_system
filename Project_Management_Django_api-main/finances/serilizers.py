from rest_framework import serializers
from peoples.models import Client, Employee
from app.models import Project
from peoples.serializers import ClientsNameSerializer, EmployeesNameSerializer
from app.serializers import ProjectsNameSerializer
from .models import BankAccounts, Invoices, Income, Expenses

# To get Project name only
class BankAccountsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = ['id', 'account_holder_name']

#Bankaccounts serializer
class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = "__all__"

    

# Invoices serializer
class InvoicesSerializer(serializers.ModelSerializer):
    project_name=ProjectsNameSerializer(read_only=True)
    client_name=ClientsNameSerializer(read_only=True)
    bank_account=BankAccountsNameSerializer(read_only=True)
    project_name_id = serializers.PrimaryKeyRelatedField(
        source = 'project_name', queryset = Project.objects.all(), write_only = True
    )
    client_name_id = serializers.PrimaryKeyRelatedField(
        source = 'client_name', queryset = Client.objects.all(), write_only = True
    )
    bank_account_id=serializers.PrimaryKeyRelatedField(
        source = 'bank_account', queryset = BankAccounts.objects.all(), write_only = True
    )
    class Meta:
        model = Invoices
        fields = "__all__"

# Income serializer
class IncomeSerializer(serializers.ModelSerializer):
    project_name=ProjectsNameSerializer(read_only=True)
    client_name=ClientsNameSerializer(read_only=True)
    bank_account=BankAccountsNameSerializer(read_only=True)
    project_name_id = serializers.PrimaryKeyRelatedField(
        source = 'project_name', queryset = Project.objects.all(), write_only = True
    )
    client_name_id = serializers.PrimaryKeyRelatedField(
        source = 'client_name', queryset = Client.objects.all(), write_only = True
    )
    bank_account_id=serializers.PrimaryKeyRelatedField(
        source = 'bank_account', queryset = BankAccounts.objects.all(), write_only = True
    )
    class Meta:
        model = Income
        fields = "__all__"

# Expenses serializer
class ExpensesSerializer(serializers.ModelSerializer):
    purchased_by=EmployeesNameSerializer(read_only=True)
    bank_account=BankAccountsNameSerializer(read_only=True)
    purchased_by_id=serializers.PrimaryKeyRelatedField(
        source = 'purchased_by', queryset = Employee.objects.all(), write_only = True
    )
    bank_account_id=serializers.PrimaryKeyRelatedField(
        source = 'bank_account', queryset = BankAccounts.objects.all(), write_only = True
    )

    class Meta:
        model = Expenses
        fields = "__all__"
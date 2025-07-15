from django.shortcuts import  get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import   BankAccounts, Invoices, Income, Expenses
from .serilizers import BankAccountsNameSerializer, BankAccountsSerializer, InvoicesSerializer, IncomeSerializer, ExpensesSerializer
from app.pagination import CustomPagination
# Create your views here.

# To get the bank account holder name
class BankAccountNameView(APIView):
    def get(self,request):
        bank_account_data = BankAccounts.objects.all().values('id', 'account_holder_name')
        ser_res = BankAccountsNameSerializer(bank_account_data, many = True)
        return Response(ser_res.data, status=status.HTTP_200_OK)
    
#bankaccounts
class BankAccountsView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class=CustomPagination
    queryset = BankAccounts.objects.all().order_by('-updated_at')
    serializer_class = BankAccountsSerializer

#invoices
class InvoicesView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class=CustomPagination
    queryset = Invoices.objects.all().order_by('-updated_at')
    serializer_class = InvoicesSerializer

#income
class IncomeView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class=CustomPagination
    queryset = Income.objects.all().order_by('-updated_at')
    serializer_class = IncomeSerializer

#expenses
class ExpensesView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class=CustomPagination
    queryset = Expenses.objects.all().order_by('-updated_at')
    serializer_class = ExpensesSerializer
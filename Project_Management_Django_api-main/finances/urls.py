from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankAccountNameView, BankAccountsView, InvoicesView, IncomeView, ExpensesView

router = DefaultRouter()
router.register(r'bank-accounts',BankAccountsView )
router.register(r'invoices',InvoicesView )
router.register(r'incomes',IncomeView )
router.register(r'expenses',ExpensesView )
urlpatterns = [
    path('', include(router.urls)),
    path('bank-accounts-name/', BankAccountNameView.as_view()),
]
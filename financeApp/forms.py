from django import forms
from .models import *


class FormCompte(forms.ModelForm):
    class Meta:
        model  = Account
        fields = ['user', 'name', 'account_type', 'balance', 'opened_on'

]
        
class FormCategory(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ['name', 'description']

class FormBudgetCategory(forms.ModelForm):
    class Meta:
        model  = BudgetCategory
        fields = ['budget', 'category', 'planned_amount']


class FormBudget(forms.ModelForm):
    class Meta:
        model  = Budget
        fields = ['user', 'name', 'total_amount', 'start_date','end_date']






class FormTransaction(forms.ModelForm):
    class Meta:
        model  = Transaction
        fields = ['account', 'category', 'amount','date','transaction_type','description']



class FormTransactionReccuring(forms.ModelForm):
    class Meta:
        model  = RecurringTransaction
        fields = ['user', 'category', 'amount','frequency','start_date','end_date','transaction_type','description']


class FormFinance(forms.ModelForm):
    class Meta:
        model  = FinancialGoal
        fields = ['user', 'name', 'target_amount','current_amount','target_date']






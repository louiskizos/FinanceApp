from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(BudgetCategory)
admin.site.register(FinancialGoal)
admin.site.register(RecurringTransaction)

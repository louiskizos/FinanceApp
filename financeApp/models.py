
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Catégorie de dépenses ou de revenus"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    """Compte bancaire de l'utilisateur"""
    ACCOUNT_TYPES = (
        ('current', 'Courant'),
        ('savings', 'Épargne'),
        ('credit', 'Crédit'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    opened_on = models.DateField()
    
    

    def __str__(self):
        return f"{self.name} ({self.account_type})"

class Transaction(models.Model):
    """Transaction financière"""
    TRANSACTION_TYPES = (
        ('income', 'Revenu'),
        ('expense', 'Dépense'),
    )
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} ({self.date})"

class Budget(models.Model):
    """Budget planifié pour une période donnée"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name

class BudgetCategory(models.Model):
    """Association entre un budget et une catégorie avec un montant prévisionnel"""
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    planned_amount = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = ('budget', 'category')

    def __str__(self):
        return f"{self.budget.name} - {self.category.name} ({self.planned_amount})"

class FinancialGoal(models.Model):
    """Objectif financier de l'utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    target_date = models.DateField()
    
    def __str__(self):
        return self.name

class RecurringTransaction(models.Model):
    """Transaction récurrente (mensuelle, annuelle, etc.)"""
    TRANSACTION_TYPES = (
        ('income', 'Revenu'),
        ('expense', 'Dépense'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    frequency = models.CharField(max_length=20)  # e.g., monthly, yearly
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} ({self.frequency})"

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User, auth
from django.db.models import Sum
from .forms import *
from django.contrib import messages


# Create your views here.

def loginPage(request):
    page = 'login.html'
    return render(request, page)

def sinInPage(request):
    page = 'create_user.html'
    
    return render(request, page)
#LogOut
def logout(request):
    auth.logout(request)
    return redirect('app:login')


#Connexion session
def connecterUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('app:home')
        else:
            message_erreur = "Desole veuillez renseigner les champs"
            return render(request, 'login.html', {'message_erreur':message_erreur})
#Create user

def CreateUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email = email).exists():
            message_erreur = "L'utilisateur existe deja"
            return render(request, 'signin.html', {'message_erreur':message_erreur})
        else:
            formulaire = User(
                username = username,
                password = password,
                email = email
            )
            formulaire.set_password(password)
            formulaire.save()
            return redirect('app:login')
# fin fin


def homePage(request):
    if request.user.is_authenticated:
       
        account = Account.objects.aggregate(total = Sum('balance'))['total']
        depense = Transaction.objects.aggregate(total = Sum('amount'))['total']
        total_trans = Transaction.objects.count()
        total_pourc = (depense / account) * 100
        
        if account is None:
            account = 0.00
        if depense is None:
            depense = 0.00
        
        context = {
            'count_accounts' : account,
            'count_depenes' : depense,
            'countTrans' : total_trans,
            'pourcentage' : total_pourc
        }
        page = 'index.html'
        return render(request, page, context)
    else:
        return redirect('app:login')


def accountPage(request):
    if request.user.is_authenticated:
        
        page = 'account.html'
        return render(request, page)
    else:
        return redirect('app:404')
    
def notFounPage(request):
    if request.user.is_authenticated:
        
        page = '404.html'
        return render(request, page)
    else:
        return redirect('app:NotFound')
def categoryPage(request):
    page ='category.html'
    
    return render(request, page)
    
#Insertion d'un compte

def insert_Compte(request):
    
    if request.method == 'POST':
        form = FormCompte(request.POST)
        if form.is_valid():
            form.save()  # Enregistre le filiere dans la base de données
            return redirect('app:home')  # Redirection après succès
    else:
        form = FormCompte()

    return render(request,  'app:home', {'form': form})

def insert_Category(request):
    
    if request.method == 'POST':
        form = FormCategory(request.POST)
        if form.is_valid():
            form.save()  # Enregistre le filiere dans la base de données
            return redirect('app:home')  # Redirection après succès
    else:
        form = FormCategory()

    return render(request,  'app:home', {'form': form})

# Catégories de budget

def catBudgetPage(request):
    budgets = Budget.objects.all()
    category = Category.objects.all()
    page = 'budgCat.html'
    context = {
        'categories':category,
        'budgets': budgets
    }
    return render(request,page, context)


def insert_catBudget(request):
    
    if request.method == 'POST':
        budget = request.POST.get('budget')
        category = request.POST.get('category')
        planned_amount = request.POST.get('planned_amount')
        if BudgetCategory.objects.filter(budget = budget).exists():
            budgets = Budget.objects.all()
            category = Category.objects.all()
            page = 'budgCat.html'
            context = {
                        'categories':category,
                        'budgets': budgets,
                        'message_erreur':message_erreur
                        }
            message_erreur = "Ses informations existent deja"
            return render(request, 'budgCat.html', context)
        else:
            formulaire = BudgetCategory(
                budget = budget,
                category = category,
                planned_amount = planned_amount
            )
            #formulaire.set_password(password)
            formulaire.save()
            #return redirect('app:login')
            


#Fin

# ============== Transaction ==============

def transaPage(request):
    
    page = 'transaction.html'
    account = Account.objects.all()
    category = Category.objects.all()
    
    context = {
        'categories':category,
        'accounts': account
    }
    return render(request, page, context)


def insert_Transaction(request):
    if request.method == 'POST':
        form = FormTransaction(request.POST)
        
        if form.is_valid():
            montant = form.cleaned_data['amount']
            id_account = form.cleaned_data['account'].id  # Récupérez l'ID du compte

            try:
                compte = Account.objects.get(id=id_account)
                
                if montant > compte.balance:
                    messages.error(request, "Le montant dépasse le solde disponible.")
                    context = {
                        'form': form,
                        'categories': Category.objects.all(),
                        'accounts': Account.objects.all(),
                        'message_erreur': "Le montant dépasse le solde disponible.",
                        'update': compte.balance
                    }
                    return render(request, 'transaction.html', context)

                # Si le montant est valide, procédez avec la transaction
                compte.balance -= montant
                compte.save()  # Mettez à jour le compte existant
                
                # Enregistrez la transaction ici (si nécessaire)
                form.save()

                return redirect('app:home')

            except Account.DoesNotExist:
                messages.error(request, "Le compte spécifié n'existe pas.")
                context = {
                    'form': form,
                    'categories': Category.objects.all(),
                    'accounts': Account.objects.all()
                }
                return render(request, 'transaction.html', context)

    else:
        form = FormTransaction()

    context = {
        'form': form,
        'categories': Category.objects.all(),
        'accounts': Account.objects.all()
    }
    return render(request, 'transaction.html', context)


# Fin

# Curreng Tran

def curringPage(request):
    
    if request.user.is_authenticated:
        cat =  Category.objects.all()
        context = {
            'categories' : cat
        }
        page = 'ruccingTrans.html'
        return render(request, page, context)
    else:
        return redirect('app:404')
    
def insert_Reccuring(request):
    
    if request.method == 'POST':
        
        form = FormTransactionReccuring(request.POST)
        if form.is_valid():
            form.save()  # Enregistre le filiere dans la base de données
            return redirect('app:home')  # Redirection après succès
    else:
        form = FormTransactionReccuring()

    return render(request,  'app:home', {'form': form})

#   Fin 

# Finan

def financePage(request):
    page = 'finance.html'
    return render(request, page)



def insert_Finance(request):
    
    if request.method == 'POST':
        
        form = FormFinance(request.POST)
        if form.is_valid():
            form.save()  # Enregistre 
            return redirect('app:home')  # Redirection après succès
    else:
        form = FormFinance()

    return render(request,  'app:home', {'form': form})


# Fin

# Budget

def budgetPage(request):
    
    page = 'budget.html'
    
    return render(request, page)


def insert_Budget(request):
    
    if request.method == 'POST':
        
        form = FormBudget(request.POST)
        if form.is_valid():
            form.save()  # Enregistre 
            return redirect('app:home')  # Redirection après succès
    else:
        form = FormBudget()

    return render(request,  'app:home', {'form': form})


# Table 

def tablePage(request):
    
    if request.user.is_authenticated:
        depense = Transaction.objects.all()
        
        context = {
            'depenses' : depense
        }
        page = 'tables.html'
       
        return render(request, page, context)
    else:
        return redirect('app:404')
    
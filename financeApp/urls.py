from django.urls import path
from .views import *

app_name = "app"
urlpatterns = [
   
    path('', homePage, name='home'),
    path('login', loginPage, name='login'),#Ca affiche la page se connecter a un compte
    path('sinIn', sinInPage, name='sinIn'), #Ca affiche la page creer un compte
    path('CreationUser', CreateUser, name='CreationUser'), #Creation 
    path('Seconnecter', connecterUser, name='Seconnecter'),
    path('Deconnexion', logout, name='Deconnexion'),
    path('Account', accountPage, name='Account'),
    path('NotFound', notFounPage, name='NotFound'),
    path('ajouter', insert_Compte, name='ajouter'),
    #debut categorie
    path('Category', categoryPage, name='Category'),
    path('cat_insert', insert_Category, name='cat_insert'),
    # fin 
    # debut Cat Budget
    path('Categorie_Budget', catBudgetPage, name='Categorie_Budget'),
    path('catBudget_insert', insert_catBudget, name='catBudget_insert'),
    #fin
    #tams
    path('Transaction', transaPage, name='Transaction'),
    path('Insert_transaction', insert_Transaction, name='Insert_transaction'),
    path('Currering_transaction', curringPage, name='Currering_transaction'),
    path('Insert_Retransaction', insert_Reccuring, name='Insert_Retransaction'),
    #Fin
    # Finance
    path('Finance', financePage, name='Finance'),
    path('Insert_Finance', insert_Finance, name='Insert_Finance'),
    #Budget
    path('Budget', budgetPage, name='Budget'),
    path('Insert_Budget', insert_Budget, name='Insert_Budget'),
    
    # Table
    path('Table', tablePage, name='Table')
]
from django.urls import path
from .views import add_expense, show_balances, signin, signout, signup, home

urlpatterns = [
    path('', home, name='home'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('add-expense/', add_expense, name='add-expense'),
    path('show-balances/', show_balances, name='show-blances')
]
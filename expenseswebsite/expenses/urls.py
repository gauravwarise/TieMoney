from django.urls import path
from .import views 
from django.contrib.auth.decorators import login_required

urlpatterns=[
    path('', login_required(views.index), name="expenses"),
    path('add-expense', views.add_expense, name="add_expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name="edit_expenses"),
    path('delete-expense/<int:id>', views.delete_expense, name="delete_expenses"),


]
from django.urls import path
from .import views 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


urlpatterns=[
    path('expenses', login_required(views.index , login_url="login"), name="expenses"),
    path('add-expense', views.add_expense, name="add_expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name="edit_expenses"),
    path('delete-expense/<int:id>', views.delete_expense, name="delete_expenses"),
    path('search-expenses', csrf_exempt(views.search_expenses), name="search-expenses"),
    path('expense_category_summary', views.expense_category_summary,
         name="expense_category_summary"),
    path('stats', views.stats_view,
         name="stats"),
     path('expenses/<int:expense_id>/', views.expense_details, name='expense_details'),
     path('expenses/category/<str:category>/', views.category_expenses, name='category_expenses'),



]
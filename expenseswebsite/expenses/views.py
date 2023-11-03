from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences

# Create your views here.
# @login_required(login_url='/authentication/login')
@login_required
def index(request):
    print("==========================session data",request.session)
    print(request.user)
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner = request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    currency = UserPreferences.objects.get(user = request.user).currency
    context = {
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency
    }
    user = request.user
    if user.is_authenticated:
        return render(request, 'expenses/index.html', context)
    else:
        return render(request, 'authentication/login')
    # return render(request, 'authentication/login')

def add_expense(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
        'values': request.POST
    }
    
    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expenses.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        print("=====date", date)
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expenses.html', context)
        try:
            Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
            messages.success(request, 'Expense saved successfully')
            return redirect('expenses')
        except:
            messages.error(request, 'something went wrong.. please enter valid credentials')
            return render(request, 'expenses/add_expenses.html', context)

def expense_edit(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()

    if request.method=='GET':
        context = {
            'expense':expense,
            'values':expense,
            'categories':categories
        }
        return render(request, 'expenses/edit-expense.html', context)
    else:
        messages.info(request,'Handling post form')
        return render(request, 'expenses/edit-expense.html', context)

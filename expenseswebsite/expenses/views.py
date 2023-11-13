from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
import json
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from django.shortcuts import render, get_object_or_404
import datetime



# Create your views here.
@never_cache
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            Q(amount__icontains=search_str) | 
            Q(date__icontains=search_str) | 
            Q(description__icontains=search_str) | 
            Q(category__icontains=search_str),
            owner=request.user
        )
        data = expenses.values()
        return JsonResponse(list(data), safe=False)





# @login_required(login_url='/authentication/login')
# @login_required
@never_cache
def index(request):
    print("==========================session data",request.session)
    print(request.user.is_authenticated)
    request.session['role'] = 'client'
    request.session['username'] = str(request.user)
    print("the session of user is >>>> ",request.session['username'])
    print(request.user)
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner = request.user)
    paginator = Paginator(expenses, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    # currency = UserPreferences.objects.get(user = request.user).currency
    try:
        currency = UserPreferences.objects.get(user=request.user)
    except UserPreferences.DoesNotExist:
    # Handle the case where UserPreferences does not exist for the user
        currency = None  # Or create a new UserPreferences object if needed

    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    categories_with_totals = (
        expenses.values('category')
                 .annotate(total_expense=Sum('amount'))
                 .order_by('category')
    )
    print("expense list ================", list(expenses))
    context = {
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency,
        'total_expense':total_expense,
        'categories_with_totals':categories_with_totals
    }
    print(context)
    user = request.user
    

    if user.is_authenticated:
        return render(request, 'expenses/index.html', context)
    else:
        return render(request, 'authentication/login')
    # return render(request, 'authentication/login')

@never_cache
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


def expense_details(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, owner=request.user)

    context = {
        'expense': expense,
    }
    print("expense details ============",context)
    return render(request, 'expenses/expense_details.html', context)

def category_expenses(request, category):
    category_expenses = Expense.objects.filter(owner=request.user, category=category)
    total_expense = category_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'category': category,
        'category_expenses': category_expenses,
        'total_expense': total_expense,
        'currency': UserPreferences.objects.get(user=request.user).currency,
    }

    return render(request, 'expenses/category_expenses.html', context)


@never_cache
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
    if request.method =='POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expenses.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        print("=====date", date)
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expenses.html', context)
        try:
            # Expense.objects.create(owner=request.user, amount=amount, date=date,
            #                    category=category, description=description)

            expense.owner=request.user
            expense.amount=amount 
            expense.date=date
            expense.category=category 
            expense.description=description

            expense.save()
            messages.success(request, 'Expense updated successfully')

            return redirect('expenses')
        except:
            messages.error(request, 'something went wrong.. please enter valid credentials')
            return render(request, 'expenses/edit-expenses.html', context)
            
@never_cache
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')

@never_cache
def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)
    print("==================================",finalrep)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

@never_cache
def stats_view(request):
    print("stats loaded ===================")
    return render(request, 'expenses/stats.html')
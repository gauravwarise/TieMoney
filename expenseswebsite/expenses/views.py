from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='/authentication/login')
@login_required
def index(request):
    print("==========================session data",request.session)
    user = request.user
    if user.is_authenticated:
        return render(request, 'expenses/index.html')
    else:
        return render(request, 'authentication/login')

def add_expense(request):
    return render(request, 'expenses/add_expenses.html')

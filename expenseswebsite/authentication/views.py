from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
# import validate_email 
from validate_email import validate_email
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

from django.contrib import messages
from django.core.mail import EmailMessage
# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        print(email)
        if not validate_email(email):
            return JsonResponse(
                {
                    'email_error':'email is invalid',
                    },
                    status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    'email_error':'sorry email in use, choose another one ',
                    },
                    status=409)
        return JsonResponse({'email_valid':True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse(
                {
                    'username_error':'username should only contain alphanumeric characters',
                    },
                    status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {
                    'username_error':'sorry username in use, choose another one ',
                    },
                    status=409)
        return JsonResponse({'username_valid':True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html') 
    def post(self,request):
        #get user data
        #validate
        #create user account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if(len(password)<6):
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context) 
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Account succesfully created')
                return redirect('authentication/login.html') 
            else:
                messages.error(request, 'Email already exists')
        else:
            messages.error(request, 'Username already exists')    
        return render(request, 'authentication/register.html') 


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
        except Exception as ex:
            pass
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")
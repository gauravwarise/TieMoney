from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User

from django.contrib import auth
from django.contrib.auth import authenticate, login

from django.contrib import messages
# Create your views here.

from django.contrib.auth.hashers import check_password





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
    
    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        # messages.success(request, 'success whatsapp')

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email, password = password)
                # user.set_password(password)
                user.is_active = True
                user.save()
                # current_site = get_current_site(request)
                # email_body = {
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #     'token': account_activation_token.make_token(user),
                # }

                # link = reverse('activate', kwargs={
                #                'uidb64': email_body['uid'], 'token': email_body['token']})

                # email_subject = 'Activate your account'

                # activate_url = 'http://'+current_site.domain+link

                # email = EmailMessage(
                #     email_subject,
                #     'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                #     'noreply@semycolon.com',
                #     [email],
                # )
                # email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)

        # user = authenticate(request=request,username=username, password=password)
        # print(user.password)


        # # The stored hashed password
        # stored_password = "pbkdf2_sha256$600000$OaAsdFeG5As91TxU9QPMmI$arCnv5pftsyKIoa4HPs2zLfyZEO6ZH14i7c8oMVaJRs="

        # # The user's entered password
        # user_password = password

        # # Check if the user's entered password matches the stored hashed password
        # if check_password(user_password, stored_password):
        #     print("===========Password is correct.")
        # else:
        #     print("=============Password is incorrect.")

        # if User.objects.filter(username=username).exists():
        #     print("========== valid username")

        # if User.objects.filter(password=password).exists():
        #     print("========== valid password")
        # # user = User.objects.get(username=username and password=password)
        # user = User.objects.get(username=username)

        # print("userpassword is .....................",user.password)

        if username and password:
            user = authenticate(username=username, password=password)
            print(user)

            if user is not None:
                print("============================")
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')

    # def post(self, request):
    #     username = request.POST["username"]
    #     password = request.POST["password"]
    #     print("=============== ", username, password)

    #     if username and password:
    #         user = auth.authenticate(username = username, password=password)
    #         print(user)
    #         if user:
    #             if user.is_active:
    #                 auth.login(request, user)
    #                 messages.success(request, "Welcome, " + user.username + " you are now logged in...")
    #             messages.error(request, "Account is not active, please check your email...")
    #             return render(request, 'authentication/login.html')
    #         messages.error(request, "Invalid credentials, try again...")
    #         return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been lagged out")
        request.session.flush() 
        print("==========================session data after logout",request.session)
        if not request.session:
            print("Session is empty.")
        else:
            print("Session is not empty.")


        return redirect('login')


        
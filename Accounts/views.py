from django.shortcuts import render, redirect
from Accounts.models import Account
from django.contrib import messages, auth
from trycourier import Courier
from . models import Account
from django.views.decorators.csrf import csrf_exempt

client = Courier(auth_token="pk_prod_TG1GS5TYWYMN47QGJZGXG1YBXQJM")

@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            print(user)
            auth.login(request, user)
            return redirect('home')
        else:
            # print(user)
            messages.warning(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'login.html')

@csrf_exempt
def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        username = request.POST.get('uname')
        print(username)
     
        try:
            try:
                if Account.objects.get(username=username):
                    messages.error(request, 'Username already exists')
                    return redirect('signup')
            except:       
                user = Account(username=username, email=email, password=password, phone_number=phone)
                user.save()
                resp = client.send_message(
                message={
                    "to": {
                    "email": "kunalpatil970730@gmail.com",
                    },
                    "template": "JTBZ16M271MT47GSMY9VVRS8P2E4",
                    "data": {
                        'user' : username,
                    },
                }
                )

                print(resp['requestId'])
                return redirect('login')
        except:
            messages.error(request, 'User already exists')
            return redirect('signup')
    return render(request, 'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

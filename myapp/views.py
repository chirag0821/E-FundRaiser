from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
# Create your views here.
def home(request):
    return HttpResponse("This is home page")

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        
        if len(username) > 10:
            print("greater than 10")
            messages.error(request,"username must be less than 10 characters!!")
        
        myuser = User.objects.create_user(username,email,password)
        myuser.save()
        messages.success(request,"Your account has been succesfully created")
        return redirect('/login')
    else:
        return render(request,'signup.html')
    
def login(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username = loginusername, password = loginpassword)
        
        if user is not None:
            auth_login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('/welcome')
        else:
            messages.error(request,"Wrong credentials In")
            return redirect('/login')
        
    return render(request,'signin.html')

def logout(request):
    auth_logout(request)
    messages.success(request,"Succesfully Logged Out")
    return redirect('/login')

def welcome(request):
    return render(request,'welcome.html')

def new_startup(request):
    return render(request, 'new_startup.html')    


def faq(request):
    return render(request, 'faq.html')

def welcome(request):
    return render(request, 'welcome.html')

def startup(request):
    return render(request, 'startup-details.html')

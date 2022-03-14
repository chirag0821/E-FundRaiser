from turtle import title
from unicodedata import name
from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from myapp.models import Startups,Uploads,Investments, Founders,Uploads #models.py  
from django.contrib.auth import get_user_model
import re

Users = get_user_model()

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

def register_startup(request):
    if request.method == 'POST':  
     # request.FILES:
        title = request.POST['title']
        firm_name = request.POST['firm_name']
        email = request.POST['email']
        start_date = request.POST['start-date']
        contact_no = request.POST['contact-no']
        brief_desc = request.POST['brief_summary']
        description = request.POST['details']
        valuation = request.POST['current_valuation']
        expected_fund = request.POST['expected_fund']
        address = request.POST['address']  
        founders = [key for key in request.POST if key.startswith("founder")]
        investors = len([key for key in request.POST if key.startswith("investor")])
        images = request.POST.get('images', [])
        documents = request.POST.get('documents', [])

        new_startup = Startups(title=title, firm_name=firm_name, email=email, start_date=start_date, 
        contact_no=contact_no, brief_desc=brief_desc, description=description, valuation=valuation, 
        expected_fund=expected_fund, address=address)
        new_startup.save()

        for inv_index in range(1, investors + 1):
            Investments(startup=new_startup, user_id=request.user.id,
                        investor=request.POST[f'investor_{inv_index}'], stake=request.POST[f'stake_{inv_index}'], amount=request.POST[f'amount_{inv_index}']).save()
                        
        for founder in founders:
            Founders(startup=new_startup, user_id=request.user.id, name=request.POST[founder]).save()

        for image in images:
            Uploads(startup=new_startup, type="image", file=image).save()
        
        for document in documents:
            Uploads(startup=new_startup, type="document", file=document).save()

        return redirect('/')



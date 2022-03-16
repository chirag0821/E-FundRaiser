from turtle import title
from unicodedata import name
from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from myapp.models import Startups,Uploads,Investments, Founders,Uploads, UseUsers #models.py  
from django.contrib.auth import get_user_model
import re
from django.contrib.auth.decorators import login_required


Users = get_user_model()

# Create your views here.

def local(request):
    return redirect('/welcome')
    
def register(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            username = request.POST['username']
            
            if len(username) > 10:
                print("greater than 10")
                messages.error(request,"username must be less than 10 characters!!")
                return redirect('/register')
            
            myuser = User.objects.create_user(username,email,password)
            myuser.save()
            UseUsers.objects.create(name=username, user=myuser)
            messages.success(request,"Your account has been succesfully created")
            return redirect('/login')
        except:
            messages.error(request, "Username or Email already taken")
            return redirect('/register')

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
            return redirect('/home')
        else:
            messages.error(request,"Wrong credentials In")
            return redirect('/login')
        
    return render(request,'signin.html')

def logout(request):
    auth_logout(request)
    messages.success(request,"Succesfully Logged Out")
    return redirect('/login')

@login_required(login_url='/login')
def new_startup(request):
    return render(request, 'new_startup.html')    


def faq(request):
    return render(request, 'faq.html')

def welcome(request):
    return render(request, 'landing_page.html')


@login_required(login_url='/login')
def home(request):
    startups = Startups.objects.all()
    for s in startups:
        try:
            img = s.uploads_set.filter(type="image").first().file.url
        except AttributeError:
            img = '/static/images/alt-startup-img.jpg'
        s.img = img

    return render(request, 'home.html',{'startups':startups})

@login_required(login_url='/login')
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
        images = request.FILES.getlist('images')
        documents = request.FILES.getlist('documents')

        new_startup = Startups(title=title, firm_name=firm_name, email=email, start_date=start_date, 
        contact_no=contact_no, brief_desc=brief_desc, description=description, valuation=valuation, 
        expected_fund=expected_fund, address=address)
        new_startup.save()

        for inv_index in range(1, investors + 1):
            Investments(startup=new_startup,
                        investor=request.POST[f'investor_{inv_index}'], stake=request.POST[f'stake_{inv_index}'], amount=request.POST[f'amount_{inv_index}']).save()
                        
        for founder in founders:
            Founders(startup=new_startup, user_id=request.user.id, name=request.POST[founder]).save()

        for image in images:
            Uploads(startup=new_startup, type="image", file=image).save()
        
        for document in documents:
            Uploads(startup=new_startup, type="document", file=document).save()
        messages.success(request,"Your startup registered succesfully")
        return redirect('/home')

@login_required(login_url='/login')
def investors(request):
    investments = Investments.objects.exclude(user_id = None)
    return render(request, 'investors.html', {'investments': investments})


@login_required(login_url='/login')
def account(request):
    user = UseUsers.objects.filter(user=request.user).first()
    if(request.method == 'POST'):
        user.name = request.POST.get('uname')
        user.contact_no = request.POST.get('ucontact')
        user.save()
        messages.success(request,"Your data has been updated succesfully!!")
        
    try:
        name = user.name
        phone = user.contact_no
    except Exception:
        name = ''
        phone = ''
        
    founders = Founders.objects.filter(user = request.user)
    investments = Investments.objects.filter(user = request.user)
    return render(request, 'account.html',{'name':name, 'phone':phone,'founders': founders,'investments': investments})

# /startup?id=<id>
@login_required(login_url='/login')
def startup(request):
    try:
        startup = Startups.objects.get(id=request.GET['id'])
        uploads = startup.uploads_set
        return render(request, 'view-startup.html', {'startup': startup, 'founders': startup.founders_set.all(), 'investments': startup.investments_set.all(), 'images': uploads.filter(type="image"), 'documents': uploads.filter(type="document")})
    except Exception:
        return redirect('/home')

def about_us(request):
    return render(request, 'about_us.html')

@login_required(login_url='/login')
def invest(request):
    try:
        startup = Startups.objects.get(id=request.POST.get('startup_id'))
        amount = int(request.POST.get('amount'))
        stake = ((amount*100) / startup.valuation)
        startup.investments_set.create(amount=amount, stake=stake, user=request.user, investor=UseUsers.objects.filter(user=request.user).first().name)
        messages.success(request, "Investment succesful!!")
        return redirect('/startup?id={}'.format(request.POST.get("startup_id")))
        
    except Exception:
        messages.error(request, "Investment failed!!")
        return redirect('/startup?id={}'.format(request.POST.get("startup_id")))

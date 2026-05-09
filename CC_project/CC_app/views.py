from django.shortcuts import render,redirect
from CC_app.models import *
from CC_app.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from datetime import date
from django.db.models import Sum , Count
from django.contrib.auth.forms import AuthenticationForm


##explanation :


#Suppose your models are like this:

# class User(AbstractUser):
#     pass

# and:

# class BasicInfoModel(models.Model):

#     user_info = models.OneToOneField(User, on_delete=models.CASCADE)

#     bmr = models.FloatField()

# Now database visually:

# User Table :

# id	username
# 1	     rony

# BasicInfoModel Table : 

# id	user_info	     bmr
# 1	     rony	        2400

# Step by Step:

# request.user

# Gets logged-in user.

# Example:

# rony

# request.user.user_info :

# Gets related BasicInfoModel.

# Example:

# BasicInfoModel object

# request.user.user_info.bmr:

# Gets BMR field from that object.

# Example:

# 2400



# Next Query: 

# today_consumed_data = ConsumeCalories.objects.filter(
#     consumed_by = current_user,
#     created_by = today
# )

# This means:

# Get all calorie data:

# consumed by current user and created today

# supposed database : 

# | Food   | Calorie | consumed_by | created_by |
# | ------ | ------- | ----------- | ---------- |
# | Rice   | 300     | rony        | today      |
# | Burger | 500     | rony        | today      |
# | Coke   | 150     | rony        | yesterday  |
# | Pizza  | 700     | other user  | today      |

# this filter returns only : 

# | Food   | Calorie |
# | ------ | ------- |
# | Rice   | 300     |
# | Burger | 500     |

# Because:

# ✅ user = rony

# ✅ date = today

# Meaning of filter():

# Give me only matching rows.



from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login

from datetime import date
from django.db.models import Sum,Count
from django.contrib.auth.forms import AuthenticationForm

from CC_app.models import*
from CC_app.forms import *

def register_page(request):
    if request.method =='POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,'Registration successful')
            return redirect('login_page')
    else:
        form_data = RegistrationForm()
    context={
            'form_data' : form_data,
            'form_title' : 'User registration form',
            'form_btn' : 'Register',
        }
    return render(request,'master/base-form.html',context)
    
def login_page(request):
    
    form_data = AuthenticationForm(request, data=request.POST)
    if request.method=='POST':
        if form_data.is_valid():
            user=form_data.get_user()
            login(request,user)
            return redirect('dashboard_page')
    
    context={
        'form_data':form_data,
        'form_title' : 'User login page',
        'form_btn' : 'LOGIN',
    }
    
    return render(request,'master/base-form.html',context)
@login_required
def dashboard_page(request):
    current_user = request.user

    try:
        bmr = round(request.user.user_info.bmr,2)
    except:
        bmr = 0

    today = date.today()

    today_consumed_data = ConsumedCalories.objects.filter(
        consumed_by=current_user,
        created_by=today
    )

    total_consumed_calories = today_consumed_data.aggregate(
        total_calorie=Sum('calorie'),
        total_count=Count('calorie')
    )

    total_caloire = total_consumed_calories['total_calorie'] or 0

    less_more = bmr-total_caloire

    if bmr > total_caloire:
        suggestion = 'besi kha calorie kom'
    else:
        suggestion = 'kom kha calorie beshi'

    context = {
        'required_calories': bmr,
        'today_consumed_data': today_consumed_data,
        'consumed_calories': total_caloire,
        'total_count': total_consumed_calories['total_count'],
        'less_more': less_more,
        'suggestion': suggestion,
    }

    return render(request,'dashboard.html',context)

@login_required
def logout_page(request):
    logout(request)
    messages.success(request,'Logout Successfully')
    return redirect('login_page')
@login_required
def profile_page(request):
    return render(request,'profile.html')
@login_required
def update_profile(request):
    try :
        current_user=request.user.user_info
    except:
        current_user=None
    if request.method=='POST':
        form_data = ProfileUpdateForm(request.POST,instance=current_user)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.user = request.user
            weight = data.weight
            height = data.height
            age = data.age 
            if data.gender=='Male':
                bmr_calculate = 66.47 +(13.75*weight)+(5.003*height)-(6.755*age)
            else:
                bmr_calculate = 655.1 +(9.563*weight)+(1.850*height)-(4.676*age)
            data.bmr=bmr_calculate
            data.save()
            messages.success(request,'Profile update successfully')
            return redirect('profile_page')
    form_data=ProfileUpdateForm(instance=current_user)
    context={
        'form_data' : form_data,
        'form_title': 'update profile info',
        'form_btn': 'Update'
    }
                
                
    return render(request,'master/base-form.html',context)


def calorie_list(request):
    consumed_data = ConsumedCalories.objects.filter(consumed_by=request.user)
    context={
        'consumed_data' : consumed_data
    }
    return render(request,'calorie_list.html',context)

def add_calorie(request):
    if request.method=='POST':
        form_data = ConsumedCalorieForm(request.POST)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.consumed_by = request.user
            data.save()
            messages.success(request,'Successful')
            return redirect('calorie_list')
        
    form_data=ConsumedCalorieForm()
    context={
        'form_data' : form_data,
        'form_title': 'add calorie info',
        'form_btn': 'add calorie'
    }
    return render(request,'master/base-form.html',context)


def update_calorie(request,id):
    try:
        data=ConsumedCalories.objects.get(id=id)
    except:
        data=None
        
    if request.method=='POST':
        form_data = ConsumedCalorieForm(request.POST,instance=data)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.consumed_by = request.user
            data.save()
            messages.success(request,'Successful')
            return redirect('calorie_list')
        
    form_data=ConsumedCalorieForm(instance=data)
    context={
        'form_data' : form_data,
        'form_title': 'update calorie info',
        'form_btn': 'update calorie'
    }
    return render(request,'master/base-form.html',context)

def delete_calorie(request,id):
    try:
        data=ConsumedCalories.objects.get(id=id)
    except:
        data=None
    if data:
        data.delete()
    messages.success(request,'Successfully')
    return redirect('calorie_list')
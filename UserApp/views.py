from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse

def login_user(request):
    if request.method == "GET":
        return render(request,"login.html")
    else:
        uname = request.POST.get("uname")
        pwd = request.POST.get("pwd")            
        user = authenticate(username=uname, password=pwd)
        if user is not None:
            login(request,user) 
            return redirect(homepage)
        else:                      
            return redirect(login_user)
        

def homepage(request):
    return render(request,"homepage.html")

def Register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect(login_user)
        
    return render(request,"signup.html")
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from PostApp.models import Post
from django.contrib.auth.decorators import login_required


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
        
@login_required
def homepage(request):
    post = Post.objects.all().order_by('-created_at')
    return render(request,"homepage.html",{"posts":post})

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


def logout_user(request):
    logout(request)	
    return redirect(homepage)

def profile(request):
    posts = Post.objects.filter(user=request.user)
    return render(request,"profile.html",{"posts":posts})
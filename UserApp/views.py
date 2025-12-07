from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from PostApp.models import Post
from django.contrib.auth.decorators import login_required
from UserApp.models import Profile,Follower

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
    following_users = []
    if request.user.is_authenticated:
        following_users = Follower.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
    return render(request,"homepage.html",{"posts":post, "following_users": following_users})

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
            profile = Profile.objects.create(user=user)
            profile.save()
            login(request, user)
            return redirect(login_user)
        
    return render(request,"signup.html")


def logout_user(request):
    logout(request)	
    return redirect(homepage)

def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user)
    followers_count = Follower.objects.filter(following=request.user).count()
    following_count = Follower.objects.filter(follower=request.user).count()
    return render(request,"profile.html",{"posts":posts,
                                          "followers_count": followers_count,
                                          "following_count": following_count,
                                          "profile":profile})


def follow_user(request,user_id):
    user_to_follow = User.objects.get(id=user_id)

    if user_to_follow == request.user:
        return redirect(homepage)
    
    follow, created = Follower.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    if not created:
        follow.delete()
        return redirect(homepage)

    return redirect(homepage)

def edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        username = request.POST.get("username")
        bio = request.POST.get("bio")

        if request.user.username != username:
            user.username = username
            user.save()

        profile.bio = bio
        if 'image' in request.FILES:
            profile.profile_image = request.FILES['image']
        profile.save()
        return redirect(user_profile)
    return render(request,"editProfile.html",{"profile":profile})
    

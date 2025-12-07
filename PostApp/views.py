from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from UserApp.models import Profile

def createPost(request):
    if request.method == "POST":
        text = request.POST.get("caption")
        image = request.FILES.get('image')

        if image:
            post = Post(user=request.user,caption=text,image_url=image)
            post.save()
            return redirect("/")

    return render(request,"createPost.html")


def mypost(request):
    posts = Post.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    return render(request,'MyPost.html',{"posts":posts,"profile":profile})



def post_update(request,pid):
    post = get_object_or_404(Post,pk=pid,user=request.user)
    if request.method == "POST":
        caption = request.POST.get("caption")
        post.caption = caption

        if 'image' in request.FILES:
            post.image_url = request.FILES['image']
        post.save()

        return redirect(mypost)

    return render(request, "updatePost.html", {"post":post})

def post_delete(request,pid):
    post = get_object_or_404(Post,pk=pid,user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect(mypost)
    return redirect(mypost)



from django.shortcuts import render, redirect
from .models import Post


def createPost(request):
    if request.method == "POST":
        text = request.POST.get("caption")
        image = request.FILES.get('image')

        if image:
            post = Post(user=request.user,caption=text,image_url=image)
            post.save()
            return redirect("/homepage")

    return render(request,"createPost.html")

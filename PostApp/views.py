from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count,Exists, OuterRef
from django.http import JsonResponse
from django.utils.timesince import timesince
from .models import Post, Like, Comment
from UserApp.models import Profile

def createPost(request):
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == "POST":
        text = request.POST.get("caption")
        image = request.FILES.get('image')

        if image:
            post = Post(user=request.user,caption=text,image_url=image)
            post.save()
            return redirect("/")

    return render(request,"createPost.html",{"profile":profile})


def mypost(request):
    posts = (Post.objects.filter(user=request.user).annotate(
            total_likes=Count('likes', distinct=True),
            total_comments=Count('comments', distinct=True)
        )
        .order_by('-id')
    )
    profile = Profile.objects.filter(user=request.user).first()
    user_likes = set(
        Like.objects.filter(user=request.user, post__in=posts)
            .values_list("post_id", flat=True)
    )
    return render(request, "MyPost.html", {
        "posts": posts,
        "profile": profile,
        "user_likes": user_likes
    })



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


def toggle_like(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        like = Like.objects.filter(post=post, user=request.user).first()

        if like:
            like.delete()
            liked = False
        else:
            Like.objects.create(post=post, user=request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'total_likes': Like.objects.filter(post=post).count()
        })


def add_comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        text = request.POST.get("text")

        post = get_object_or_404(Post, id=post_id)

        if text.strip() == "":
            return JsonResponse({"error": "Empty comment not allowed"}, status=400)

        comment = Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )

        return JsonResponse({
            "username": comment.user.username,
            "text": comment.text,
            "created": timesince(comment.created_at) + " ago"
        })
    

def get_comments(request, post_id):
    comments = Comment.objects.filter(post_id=post_id).order_by("-created_at")

    data = []
    for c in comments:
        data.append({
            "username": c.user.username,
            "text": c.text,
            "time": timesince(c.created_at) + " ago"
        })

    return JsonResponse(data, safe=False)
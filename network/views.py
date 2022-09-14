from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt


from .models import User, Post, Follow

def index(request):
    #paginator 
    all_posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(all_posts,10)

    try: 
        posts = paginator.get_page(request.GET.get('page'))
    except:
        posts = paginator.page(1)

    
    return render(request, "network/index.html", {
        "posts": posts,
        "paginator": paginator,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newpost(request):
    if request.method == 'POST':
        author = User.objects.get(username = request.user)
        content = request.POST["content"]

        new_post = Post(author=author, content = content)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))

def profile(request, author):
    #determine the number of following
    author = User.objects.get(username=author)
    
    try: 
        num_following = len(Follow.objects.get(user = author).following.all())
    except:
        num_following = 0
    
    # determine the number of followers
    num_followers = len(author.following.all())

    # get author's posts
    
    all_posts = Post.objects.filter(author = author).order_by('-timestamp')
    paginator = Paginator(all_posts,10)

    # Follow or unfollow
    user = User.objects.get(username = request.user)
    try:
        following = Follow.objects.get(user = user).following.all()
    except:
        following = []

    if author in following:
        is_following = True
    else:
        is_following = False

    # Paginator
    try: 
        posts = paginator.get_page(request.GET.get('page'))
    except:
        posts = paginator.page(1)

    return render(request, "network/profile.html", {
        "profile": author,
        "posts": posts,
        "posts_number": len(posts),
        "followers": num_followers,
        "following": num_following,
        "paginator": paginator,
        "is_following": is_following
    })

def following(request):
    try:
        following = Follow.objects.get(user = request.user).following.all()
    except:
        following = []
        
    all_posts = Post.objects.filter(author__in = following).order_by('-timestamp')

    paginator = Paginator(all_posts,10)

    try: 
        posts = paginator.get_page(request.GET.get('page'))
    except:
        posts = paginator.page(1)

    return render(request, "network/following.html", {
        "posts": posts,
        "paginator": paginator,
    })

def follow(request, author):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        author = User.objects.get(username = author)

    try:
        Follow.objects.get(user = user).following.add(author)
    except:
        new_follow = Follow(user = user, following = author)
        new_follow.save()

    return HttpResponseRedirect(reverse("profile", args=(author,)))

def unfollow(request, author):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        author = User.objects.get(username = author)
    
    Follow.objects.get(user = user).following.remove(author)

    return HttpResponseRedirect(reverse("profile", args=(author,)))


@csrf_exempt
@login_required
def like(request, post_id):
    #get the post that has been liked
    try:
        post=Post.objects.get(pk = post_id)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)

    # get the user who liked the post
    user = User.objects.get(username = request.user)
    
    # Update records 
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            post.likes.add(user)
            post.likes_count = post.likes_count + 1
            post.save()
        if data.get("unlike") is not None:
            post.likes.remove(user)
            post.likes_count = post.likes_count - 1
            post.save()
        return HttpResponse(status=204)

@csrf_exempt
@login_required
def edit(request, post_id):
    # get the post we want error if it doesnt exist
    try:
        post=Post.objects.get(pk = post_id)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data['edit']
        post.save()
    return HttpResponse(status=204)
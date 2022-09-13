from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

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
        "paginator": paginator
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
        "paginator": paginator
    })

def following(request):
    following = Follow.objects.get(user = request.user).following.all()
    all_posts = Post.objects.filter(author__in = following).order_by('-timestamp')

    paginator = Paginator(all_posts,10)

    try: 
        posts = paginator.get_page(request.GET.get('page'))
    except:
        posts = paginator.page(1)

    
    return render(request, "network/following.html", {
        "posts": posts,
        "paginator": paginator
    })
    

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<str:author>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("<str:author>/follow", views.follow, name="follow"),
    path("<str:author>/unfollow", views.unfollow, name="unfollow"),

    # API Routes
    path("like/<int:post_id>", views.like, name="like"),
    path("edit/<int:post_id>", views.edit, name='edit')
]


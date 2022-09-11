from django.contrib.auth.models import AbstractUser
from django.db import models
from tkinter import CASCADE


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=280, blank=False)
    timestamp = models.DateTimeField(auto_now_add = True)
    likes = models.IntegerField(default = "0")

    def __str__(self):
        return f"On {self.timestamp}, {self.author} said {self.content}"


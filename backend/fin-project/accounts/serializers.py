from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=10)
    nickname = models.CharField(max_length=30)
    useremail = models.EmailField(max_length=254)

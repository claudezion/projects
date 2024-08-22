from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone


class User(AbstractUser):
    pass


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    starting_bid = models.CharField(max_length=10)
    current_bid = models.CharField(max_length=10, default=0.0)
    current_bid_user_id = models.IntegerField()
    url = models.URLField()
    category = models.CharField(max_length=50)
    user_id = models.IntegerField()
    status = models.CharField(max_length=5)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Bid(models.Model):
    item_id = models.IntegerField()
    user_name = models.CharField(max_length=150)
    bid = models.CharField(max_length=10)
    date = models.DateTimeField(default=django.utils.timezone.now)


class Watchlist(models.Model):
    item_id = models.IntegerField()
    user_id = models.IntegerField()
    title = models.CharField(max_length=100)


class Comment(models.Model):
    item_id = models.IntegerField()
    user_name = models.CharField(max_length=150)
    comment = models.CharField(max_length=250)
    date = models.DateTimeField(default=django.utils.timezone.now)

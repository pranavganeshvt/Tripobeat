from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# Class and Objects for Blog Page
class BlogPost(models.Model):
    title = models.CharField(max_length= 200)
    description = models.TextField()

# Class and Objects for Category Page
class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cost = models.TextField()
    image_url = models.ImageField(upload_to='images/')
    departure_details = models.TextField(default = '')
    return_details = models.TextField(default = '')
    inclusions = models.TextField(default = '')
    exclusions = models.TextField(default = '')
    access = models.TextField(default = '')
    cancel = models.TextField(default = '')
    author = models.CharField(default= "Pranav")
    date_posted = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tripobeatApp:item_page', args=[self.id])

# Class and Objects for Item Page
class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    departure_details = models.TextField()
    return_details = models.TextField()
    inclusions = models.TextField()
    exclusions = models.TextField()
    access = models.TextField()
    cancel = models.TextField()
    image_url = models.ImageField(upload_to='images/')
    author = models.CharField(default= "Pranav")
    date_posted = models.DateTimeField(default = timezone.now)


# Class and Objects for Item Page Reviews
class Review(models.Model):
    name = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.item.title

    def get_absolute_url(self):
        return reverse('tripobeatApp:item_page', args=[self.item_id])


# Class and Objects for Home Page
class Search(models.Model):
    place = models.TextField()

regular_user = {"username": "Pranav", "password": "Pranav"}
admin_user = {"username": "admin", "password": "admin"}
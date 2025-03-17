from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
class ChatMessage(models.Model):
    username = models.CharField(max_length=255)  # Store username
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.message} ({self.timestamp})"


# Create your models here.
class User(models.Model):
    email=models.EmailField(primary_key=True)
    name=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    usertype=models.CharField(max_length=100,default="buyer")
    
class Courses(models.Model):
    course_id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=100)
    course_price=models.FloatField()
    course_length=models.CharField(max_length=100)
    course_img = models.ImageField(upload_to='media/course_images/')
    course_bought=models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.course_name+" "+str(self.course_id)
    
class Cart(models.Model):
    email_use = models.EmailField()  # No default, empty allowed
    course_IDS=models.CharField(max_length=100)
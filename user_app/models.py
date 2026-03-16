from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.
class users(AbstractUser):
    usertype = models.IntegerField(default=1)
    DISTRICTS_CHOICES = [
        ('Alappuzha', 'Alappuzha'),
        ('Ernakulam', 'Ernakulam'),
        ('Idukki', 'Idukki'),
        ('Kannur', 'Kannur'),
        ('Kasaragod', 'Kasaragod'),
        ('Kollam', 'Kollam'),
        ('Kottayam', 'Kottayam'),
        ('Kozhikode', 'Kozhikode'),
        ('Malappuram', 'Malappuram'),
        ('Palakkad', 'Palakkad'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Thrissur', 'Thrissur'),
        ('Wayanad', 'Wayanad'),
    ]
    
    # No need to redefine password; Django already includes it in AbstractUser
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    place = models.CharField(max_length=100)
    district = models.CharField(max_length=50, choices=DISTRICTS_CHOICES)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    
    

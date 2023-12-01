from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
import uuid
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model
User=get_user_model()


class Profile(models.Model):
    id_user=models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = ArrayField(models.CharField(max_length=20),blank=True,default=list)
    following = ArrayField(models.CharField(max_length=20),blank=True,default=list)
    count_followers=models.IntegerField(blank=True,default=0)
    count_following=models.IntegerField(blank=True,default=0)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
class Post(models.Model):
    Post_id=models.UUIDField(primary_key=True,default=uuid.uuid4)   
    user = models.CharField(max_length=100) 
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=1000)
    created_at=models.DateTimeField(default=timezone.now())
    comments=ArrayField(models.CharField(max_length=500), blank=True,default=list)
    likes=ArrayField(models.CharField(max_length=20), blank=True,default=list)
    count_likes=models.IntegerField(blank=True,default=0)
    count_comments=models.IntegerField(blank=True,default=0)
    
    def __str__(self):
        return f'{self.user} Post'
    
class Comments(models.Model):
    commentid=models.AutoField(primary_key=True)
    comment=models.TextField(max_length=500)
    
    def __int__(self):
        return self.commentid


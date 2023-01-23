from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from djongo import models   
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime 
from django.utils.translation import ugettext_lazy as _ 
from django.utils import timezone 
import math


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model.""" 
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class UserProfile(models.Model): 
    user = models.ForeignKey('User', on_delete=models.CASCADE) 
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=10, blank=True)
    credit_details = models.CharField(max_length=16, blank=True) 
    image = models.ImageField(upload_to='IMG/', blank=True)  
    date_of_birth = models.DateField(blank = True,default=None)
    rating = models.PositiveIntegerField(blank=True,default=0)   

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class ApiCredentials(models.Model): 
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE) 
    remote_id = models.CharField( max_length = 1000, blank=True)
    secret = models.CharField(max_length = 1000, blank=True)
    created_at = models.CharField(max_length=20, blank=True) 
    username = models.CharField(max_length=70, blank=True)




class Announcement(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.PROTECT)  
    title = models.CharField(max_length=70, blank=False ) 
    street_name =  models.CharField(max_length=100) 
    coordonates =  models.CharField(max_length=100) 
    # IMG STORAGE PATH 
    image = models.ImageField(upload_to='IMGS/', blank=True) 
    annType = models.CharField(max_length=5, blank=False )
    content = models.TextField(max_length=5000) 
    tags = models.ManyToManyField('Tag')
    reward = models.PositiveSmallIntegerField( default =0, blank =True)
    created_time = models.DateTimeField(auto_now_add= True)  
    passed_time = models.CharField(max_length = 50)  


    def updateTimePassed(self):
        self.passed_time = self.whenpublished() 
        self.save()

    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.created_time

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago" 

        return ""


class Message(models.Model):
    sender_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    chat_id = models.ForeignKey('Chat', on_delete=models.PROTECT)
    registered_time = models.DateTimeField(default=datetime.now)
    edited_time = models.DateTimeField()
    is_read = models.BooleanField(default=False)
    content = models.TextField(max_length=1000)


class Chat(models.Model):
    user_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    register_date = models.DateTimeField(default=datetime.now, blank=True) 
    close_date = models.DateTimeField()  

    
class Comment(models.Model):
    announcement_id = models.ForeignKey('Comment', on_delete=models.PROTECT)
    user_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    registered_time = models.DateTimeField(default=datetime.now, blank=True)
    edited_time = models.DateTimeField()
    content = models.TextField(max_length=1000)


class Tag(models.Model):
    name = models.CharField(max_length=20, blank=False,  unique=True)



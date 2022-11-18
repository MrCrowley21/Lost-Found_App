from django import forms
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from djongo import models


class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=30, blank =False )  
    last_name = models.CharField(max_length=30, blank =True ) 
    phone = models.CharField(max_length=20, blank=True )
    location = models.CharField(max_length=10, blank=True)
    credit_details = models.CharField(max_length=16, blank=True)
    rating = models.PositiveIntegerField() 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Announcement(models.Model):
    #announcement_id = models.ObjectIdField(primary_key=True)
    user_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    #tags = ArrayField( models.CharField(max_length=1024, blank=True), default= list)
    location = models.URLField(max_length=250) 
    # IMG STORAGE PATH 
    image = models.ImageField(upload_to='IMGS/', blank=True)
    content = models.TextField(max_length=5000)
    reward = forms.FloatField(min_value=0.0)


class Message(models.Model):
    #message_id = models.ObjectIdField(primary_key=True)
    sender_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    chat_id = models.ForeignKey('Chat', on_delete=models.PROTECT)
    registered_time = models.DateTimeField()
    edited_time = models.DateTimeField()
    is_read = models.BooleanField(default=False)
    content = models.TextField(max_length=1000)


class Chat(models.Model):
    #chat_id = models.ObjectIdField(primary_key=True)
    user_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    register_date = models.DateTimeField()
    close_data = models.DateTimeField()

    
class Comment(models.Model):
   # comment_id = models.ObjectIdField(primary_key=True)
    user_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    announcement_id = models.ForeignKey('Announcement', on_delete=models.PROTECT)
    registered_time = models.DateTimeField()
    edited_time = models.DateTimeField()
    content = models.TextField(max_length=1000)



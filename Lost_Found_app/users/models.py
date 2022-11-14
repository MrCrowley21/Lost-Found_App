from djongo import models 
from django.db.models.signals import post_save
from django.dispatch import receiver  
from django.contrib.auth.models import User  


class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=30, blank =False )  
    last_name = models.CharField(max_length=30, blank =True ) 
    phone = models.CharField(max_length=20, blank=True )
    location = models.CharField(max_length=10, blank=True)
    credit_details = models.CharField(max_length = 16, blank=True)   
    rating = models.PositiveIntegerField() 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
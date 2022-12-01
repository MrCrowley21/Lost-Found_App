from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from djongo import models   
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime 
from django.utils.translation import ugettext_lazy as _

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
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=10, blank=True)
    credit_details = models.CharField(max_length=16, blank=True) 
    image = models.ImageField(upload_to='IMG/', blank=True) 
    rating = models.PositiveIntegerField(blank=True) 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Announcement(models.Model):
    #announcement_id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey('UserProfile', on_delete=models.PROTECT)  
    title = models.CharField(max_length=50, blank=False )
    location = models.URLField(max_length=250) 
    # IMG STORAGE PATH 
    image = models.ImageField(upload_to='IMGS/', blank=True) 
    annType = models.CharField(max_length=5, blank=False )
    content = models.TextField(max_length=5000) 
    tags = models.ManyToManyField('Tag')
    reward = models.PositiveSmallIntegerField( default =0, blank =True)


class Message(models.Model):
    #message_id = models.ObjectIdField(primary_key=True)
    sender_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    chat_id = models.ForeignKey('Chat', on_delete=models.PROTECT)
    registered_time = models.DateTimeField(default=datetime.now)
    edited_time = models.DateTimeField()
    is_read = models.BooleanField(default=False)
    content = models.TextField(max_length=1000)


class Chat(models.Model):
    #chat_id = models.ObjectIdField(primary_key=True)
    user_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    register_date = models.DateTimeField(default=datetime.now, blank=True) 
    close_date = models.DateTimeField()  

    
class Comment(models.Model):
   # comment_id = models.ObjectIdField(primary_key=True) 
    announcement_id = models.ForeignKey('Comment', on_delete=models.PROTECT)
    user_id = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    registered_time = models.DateTimeField(default=datetime.now, blank=True)
    edited_time = models.DateTimeField()
    content = models.TextField(max_length=1000)


class Tag(models.Model):
    name = models.CharField(max_length=10, blank=False)




from django import forms  
from databaseQueries.models import Announcement

class AnnouncementForm(forms.ModelForm):   
    class Meta: 
        model = Announcement 
        fields = ['image'] 
from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Announcement)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Comment)

from django.contrib import admin
from .models import Profile, Follower


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','bio','profile_image']

class FollowerAdmin(admin.ModelAdmin):
    list_display = ['id','follower','following']

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Follower,FollowerAdmin)

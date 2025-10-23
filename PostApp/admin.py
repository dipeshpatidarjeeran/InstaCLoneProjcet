from django.contrib import admin
from .models import Post, Comment, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user','caption','image_url','created_at']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','text','created_at']

class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','post','user']


admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Like,LikeAdmin)
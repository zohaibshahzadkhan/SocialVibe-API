from django.contrib import admin
from .models import Like, Comment, PostAttachment, Post

# Register your models here

admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(PostAttachment)
admin.site.register(Post)

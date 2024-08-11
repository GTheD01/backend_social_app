from django.contrib import admin

from .models import Post, PostAttachment, Like

# Register your models here.
admin.site.register(Post)
admin.site.register(PostAttachment)
admin.site.register(Like)


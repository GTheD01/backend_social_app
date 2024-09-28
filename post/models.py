import uuid

from django.conf import settings
from django.db import models
from django.utils.timesince import timesince
from django.utils import timezone

from users.models import UserAccount

# Create your models here.
class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(UserAccount, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    body = models.TextField(max_length=1024)
    created_by = models.ForeignKey(UserAccount, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def created_at_formatted(self):
        return timesince(self.created_at)


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to="post_attachments")
    created_by = models.ForeignKey(UserAccount,related_name="post_attachments", on_delete=models.CASCADE)

    def get_image(self):
        if (self.image):
            return settings.WEBSITE_URL +  self.image.url
        else: 
            return ""
        
        
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    body = models.TextField()
    created_by = models.ForeignKey(UserAccount, related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    attachments = models.ManyToManyField(PostAttachment, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)

    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_at',)


    def created_at_formatted(self):
        return timesince(self.created_at)


    def __str__(self):
        return self.body
    
class PopularPost(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    calculated_at = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return f"Post: {self.post.body} -- Generated at:{self.calculated_at}"
import uuid

from django.conf import settings
from django.db import models
from django.utils.timesince import timesince

from users.models import UserAccount

# Create your models here.
class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to="attachments")
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

    class Meta:
        ordering = ('-created_at',)


    def created_at_formatted(self):
        return timesince(self.created_at)


    def __str__(self):
        return self.body
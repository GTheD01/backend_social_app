import uuid

from django.db import models
from django.utils.timesince import timesince

from users.models import UserAccount

# Create your models here.
class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to="attachments")
    created_by = models.ForeignKey(UserAccount,related_name="post_attachments", on_delete=models.CASCADE)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(UserAccount, related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    
    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def __str__(self):
        return self.body
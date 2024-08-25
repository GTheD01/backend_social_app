import uuid

from django.db import models
from django.utils.timesince import timesince
from users.models import UserAccount

# Create your models here.
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    users = models.ManyToManyField(UserAccount, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def modified_at_formatted(self):
        return timesince(self.modified_at)
    

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(UserAccount, related_name='received_message', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserAccount, related_name="sent_messages", on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ('created_at',)

    def created_at_formatted(self):
        return timesince(self.created_at)
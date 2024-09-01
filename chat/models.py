import uuid

from django.db import models
from django.utils.timesince import timesince
from django.utils import timezone
from users.models import UserAccount
from datetime import  timedelta

# Create your models here.
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    users = models.ManyToManyField(UserAccount, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def modified_at_formatted(self):
        now = timezone.now()
        modified = self.modified_at
        time_difference = now - modified



        if (time_difference > timedelta(hours=24)):
            return self.modified_at.strftime("%d/%m")

        return self.modified_at.strftime("%H:%M")
    

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
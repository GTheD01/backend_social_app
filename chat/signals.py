from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message

@receiver(post_save, sender=Message)
def update_conversation_modified_at(sender, instance, created, **kwargs):
    if created and instance.conversation:
        instance.conversation.modified_at = timezone.now()
        instance.conversation.save()
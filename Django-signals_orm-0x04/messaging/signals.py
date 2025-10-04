from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving an updated Message, check if content is changed.
    If changed, log the old content into MessageHistory.
    """
    if instance.pk:  # Only if updating an existing message
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old_message.content != instance.content:
            # Save history
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )
            # Mark as edited
            instance.edited = True

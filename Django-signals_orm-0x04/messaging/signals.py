from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification


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
                old_content=old_message.content,
                edited_by=instance.edited_by if hasattr(instance, "edited_by") else None
            )
            # Mark as edited
            instance.edited = True


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Clean up related data when a User is deleted.
    - Deletes messages sent or received by the user
    - Deletes notifications belonging to the user
    - Deletes message histories where the user was the editor
    """
    # Delete messages (sender or receiver)
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications
    Notification.objects.filter(user=instance).delete()

    # Delete histories linked to this user as editor
    MessageHistory.objects.filter(edited_by=instance).delete()

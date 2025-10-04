from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)   # ✅ Track if edited
    edited_by = models.ForeignKey(                # ✅ Track who edited
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages"
    )

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content[:20]}"


class MessageHistory(models.Model):
    """
    Stores old versions of a message before edits.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_by = models.ForeignKey(                # ✅ Who made this edit
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="message_histories"
    )
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"

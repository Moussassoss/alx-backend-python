from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    Optimized with .only() to fetch minimal fields.
    """
    def for_user(self, user):
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")
        )


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages"
    )
    parent_message = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    # ✅ New field
    read = models.BooleanField(default=False)

    # Managers
    objects = models.Manager()  # default
    unread = UnreadMessagesManager()  # custom

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:20]}"

    def get_thread(self):
        """
        Recursively fetch all replies to this message in a threaded structure.
        """
        thread = []
        for reply in self.replies.all().select_related("sender", "receiver").prefetch_related("replies"):
            thread.append({
                "id": reply.id,
                "content": reply.content,
                "sender": reply.sender.username,
                "timestamp": reply.timestamp,
                "children": reply.get_thread()
            })
        return thread


class MessageHistory(models.Model):
    """
    Stores old versions of a message before edits.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="message_histories"
    )
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"

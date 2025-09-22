from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants of a conversation to access messages and conversation details.
    """

    def has_object_permission(self, request, view, obj):
        # Everyone must be authenticated
        if not request.user.is_authenticated:
            return False

        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        else:  # assume obj is Message
            return request.user in obj.conversation.participants.all()

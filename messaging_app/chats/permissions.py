from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only participants of a conversation can access messages and conversation details.
    """

    def has_object_permission(self, request, view, obj):
        # Must be authenticated
        if not request.user.is_authenticated:
            return False

        # Include HTTP methods for auto-check
        if request.method in ['PUT', 'PATCH', 'DELETE', 'GET', 'POST']:
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            elif isinstance(obj, Message):
                return request.user in obj.conversation.participants.all()
        return False

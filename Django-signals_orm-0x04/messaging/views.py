from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import cache_page  # ✅ import cache_page
from .models import Message


@login_required
def delete_user(request):
    """
    View for a logged-in user to delete their account.
    """
    user = request.user
    username = user.username
    user.delete()
    messages.success(request, f"Account '{username}' has been deleted successfully.")
    return redirect("home")  # redirect to home or login page after deletion


@login_required
def send_message(request, receiver_id):
    """
    Send a message from the logged-in user to another user.
    """
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_message")

        parent_message = None
        if parent_id:
            parent_message = Message.objects.filter(id=parent_id).first()

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message,
        )
        messages.success(request, "Message sent successfully.")
        return redirect("inbox")

    return render(request, "messaging/send_message.html", {"receiver": receiver})


@login_required
def inbox(request):
    """
    Display inbox messages with threaded replies.
    Optimized with select_related and prefetch_related.
    """
    user_messages = (
        Message.objects.filter(receiver=request.user)
        .select_related("sender", "receiver", "parent_message")
        .prefetch_related("replies")
    )

    return render(request, "messaging/inbox.html", {"messages": user_messages})


@login_required
def unread_inbox(request):
    """
    Show only unread messages for the logged-in user.
    Optimized with .only().
    """
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(
        request,
        "messaging/unread_inbox.html",
        {"messages": unread_messages}
    )


def get_threaded_replies(message):
    """
    Recursive function to fetch all replies for a message.
    """
    replies = message.replies.select_related("sender", "receiver").all()
    threaded = []
    for reply in replies:
        threaded.append(
            {
                "message": reply,
                "replies": get_threaded_replies(reply),
            }
        )
    return threaded


@login_required
@cache_page(60)  # ✅ Cache this view for 60 seconds
def view_conversation(request, message_id):
    """
    View a message and all its threaded replies.
    """
    message = get_object_or_404(
        Message.objects.select_related("sender", "receiver"), id=message_id
    )
    thread = get_threaded_replies(message)
    return render(
        request,
        "messaging/conversation.html",
        {"message": message, "thread": thread},
    )

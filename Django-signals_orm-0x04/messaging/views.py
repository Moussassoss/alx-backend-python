from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages


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

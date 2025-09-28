# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app outside 6 AM - 9 PM.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server hour
        current_hour = datetime.now().hour

        # Deny access if outside 6 AM - 9 PM
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access to the messaging app is restricted between 9 PM and 6 AM.")

        # Otherwise continue processing
        response = self.get_response(request)
        return response

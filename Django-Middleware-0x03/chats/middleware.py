import logging
from datetime import datetime
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        return self.get_response(request)

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


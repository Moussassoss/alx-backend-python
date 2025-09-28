import logging
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
from time import time
from collections import defaultdict, deque

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

class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of messages a user can send within a time window.
    Example: max 5 messages per minute per IP.
    """
    def __init__(self, get_response, max_messages=5, window_seconds=60):
        self.get_response = get_response
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        self.ip_message_times = defaultdict(deque)

    def __call__(self, request):
        # Only limit POST requests to messages
        if request.method == "POST" and request.path.startswith("/api/messages/"):
            ip = self.get_client_ip(request)
            now = time()
            timestamps = self.ip_message_times[ip]

            # Remove timestamps older than window
            while timestamps and now - timestamps[0] > self.window_seconds:
                timestamps.popleft()

            if len(timestamps) >= self.max_messages:
                return JsonResponse(
                    {"error": f"Message rate limit exceeded: {self.max_messages} per {self.window_seconds} seconds."},
                    status=429,
                )

            timestamps.append(now)
            self.ip_message_times[ip] = timestamps

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

class RolepermissionMiddleware:
    """
    Middleware to allow only admins or moderators to access specific actions.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check user role only if user is authenticated
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            if not (user.is_staff or getattr(user, 'role', None) in ['admin', 'moderator']):
                return JsonResponse(
                    {"error": "Access denied: Admins or Moderators only."},
                    status=403
                )

        # Continue processing request
        response = self.get_response(request)
        return response



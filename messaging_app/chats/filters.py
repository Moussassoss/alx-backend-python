import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages by sender, conversation, and sent_at range
    sender = django_filters.NumberFilter(field_name='sender__id')
    conversation = django_filters.NumberFilter(field_name='conversation__id')
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'sent_after', 'sent_before']

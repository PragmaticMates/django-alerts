from django import template
from django.utils.safestring import mark_safe

from ..models import Alert

register = template.Library()


@register.simple_tag(takes_context=True)
def alerts(context, tag, subject=None):
    """
    Retrieves number of unread alerts by ``tag`` for current user from request.
    Notifications could be specified by optional argument ``subject`` as well,

    Syntax::

        {% notifications 'tag' ['subject'] %}

    Example usage::

        {% notifications 'new-comments' %}             ... shows number of all unread comments of user articles
        {% notifications 'new-comments' article %}     ... shows number all unread comments of specified article
    """

    user = context['request'].user

    alerts = Alert.objects.unread().for_recipient(user).by_tag(tag)
    if subject:
        alerts = alerts.of_subject(subject)
    number = alerts.count()

    if number > 0:
        return mark_safe('<span class="badge badge-notification">%d</span>' % number)
    return ''

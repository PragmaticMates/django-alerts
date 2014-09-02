from django import template
from django.db.models import Q
from django.utils.safestring import mark_safe

from ..models import Alert

register = template.Library()


@register.simple_tag(takes_context=True)
def alerts(context, tags, *args, **kwargs):
    """
    Retrieves number of unread alerts by ``tag`` for current user from request.
    Notifications could be specified by optional argument ``subject`` as well.
    For context JSON field lookup you need to pass both ``context_attribute``
    and ``context_value`` arguments.

    Syntax::

        {% alerts 'tag' [subject=my_subject_object] [context_attribute='foo'] [context_value='bar'] %}

    Example usage::

        {% alerts 'new-comments' %}
            ... shows number of all unread comments of user articles

        {% alerts 'new-comments' subject=article %}
            ... shows number all unread comments of specified article

        {% alerts 'new-comments' context_attribute='category' context_value='100' %}
            ... shows number all unread comments of specified context
    """

    subject = kwargs.get('subject', None)
    context_attribute = kwargs.get('context_attribute', None)
    context_value = kwargs.get('context_value', None)

    if context_attribute and not context_value:
        raise ValueError(u"'context_value' argument is missing")

    if context_value and not context_attribute:
        raise ValueError(u"'context_attribute' argument is missing")

    user = context['request'].user
    tags = tags.split('|')
    alerts = Alert.objects.unread().for_recipient(user).by_tags(tags)

    if subject:
        alerts = alerts.of_subject(subject)

    if context_attribute and context_value:
        context = {context_attribute: context_value}
        alerts = alerts.in_context(context)

    number = alerts.count()
    
    if number > 0:
        return mark_safe('<span class="badge badge-notification">%d</span>' % number)
    return ''

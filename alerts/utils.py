from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_callable(kls):
    """
    Converts a string to a callable object.
    Courtesy: http://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname/452981#452981
    """
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def get_message_handler():
    message_handler = getattr(settings, 'ALERTS_MESSAGE_HANDLER', None)
    if message_handler is None:
        raise ImproperlyConfigured('ALERTS_MESSAGE_HANDLER is not set')
    return get_callable(message_handler)()

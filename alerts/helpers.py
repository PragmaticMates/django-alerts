from models import Alert


def notify(recipient, tag, subject=None, level=None):
    kwargs = {
        'recipient': recipient,
        'tag': tag,
        'subject': subject
    }
    if level is not None:
        kwargs['level'] = level
    return Alert.objects.create(**kwargs)


def mark_as_read(tag, user, subject=None, context=None):
    alerts = Alert.objects.by_tag(tag)
    if subject:
        alerts = alerts.of_subject(subject)
    if context:
        alerts = alerts.in_context(context)
    alerts.mark_as_read(user)


class AlertMessageHandler(object):
    def get_message(self, alert):
        raise NotImplementedError()

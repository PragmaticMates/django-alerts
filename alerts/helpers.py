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


class AlertMessageHandler(object):
    def get_message(self, alert):
        raise NotImplementedError()

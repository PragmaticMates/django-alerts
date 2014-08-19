from models import Alert


def notify(recipient, tag, subject=None, level=None):
    Alert.objects.create(
        recipient=recipient,
        tag=tag,
        subject=subject,
        level=level
    )


class AlertMessageHandler(object):
    def get_message(self, alert):
        raise NotImplementedError()

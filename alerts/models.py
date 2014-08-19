from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from managers import AlertManager
from utils import get_message_handler


def alert_settings(attribute):
    message_handler = get_message_handler()
    return getattr(message_handler, attribute, None)


class Alert(models.Model):
    LEVEL_INFO = 'INFO'
    LEVEL_SUCCESS = 'SUCCESS'
    LEVEL_WARNING = 'WARNING'
    LEVEL_ERROR = 'ERROR'
    LEVELS = (
        (LEVEL_INFO, _('info')),
        (LEVEL_SUCCESS, _('success')),
        (LEVEL_WARNING, _('warning')),
        (LEVEL_ERROR, _('error'))
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'recipient'), related_name='alerts')
    tag = models.CharField(verbose_name=_(u'tag'), max_length=128)
    level = models.CharField(verbose_name=_(u'level'), max_length=16, choices=LEVELS, default=LEVEL_INFO)
    subject = GenericForeignKey('subject_type', 'subject_id')
    subject_id = models.PositiveIntegerField()
    subject_type = models.ForeignKey(ContentType, related_name='alert_subject')
    is_read = models.BooleanField(_(u'read'), default=False)
    is_email_sent = models.BooleanField(_(u'email sent'), default=False)
    is_pushed = models.BooleanField(_(u'pushed'), default=False)
    created = models.DateTimeField(_(u'created'), auto_now_add=True)
    modified = models.DateTimeField(_(u'modified'), auto_now=True)
    objects = AlertManager()

    class Meta:
        db_table = 'alerts_alert'
        verbose_name = _(u'alert')
        verbose_name_plural = _(u'alerts')
        ordering = ('-created', )

    def __unicode__(self):
        return self.message

    @property
    def message(self):
        message_handler = message_handler = get_message_handler()
        return message_handler.get_message(self)

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()

    def mark_as_unread(self):
        if self.is_read:
            self.is_read = False
            self.save()

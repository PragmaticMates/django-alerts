from django.contrib import admin

from forms import AlertForm
from models import Alert
from utils import get_message_handler


class AlertAdmin(admin.ModelAdmin):
    form = AlertForm
    list_display = ('pk', 'level', 'tag_display', 'recipient', 'subject', 'is_read', 'is_email_sent', 'is_pushed', 'created')
    list_filter = ('level', 'tag')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "tag":
            kwargs['choices'] = self.tag_choices()
        return super(AlertAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def tag_choices(self):
        message_handler = get_message_handler()
        return getattr(message_handler, 'TAGS', None)

    def tag_display(self, alert):
        choices = self.tag_choices()
        choice = dict(choices).get(alert.tag, None)
        if choice is not None:
            return choice
        return alert.tag

admin.site.register(Alert, AlertAdmin)

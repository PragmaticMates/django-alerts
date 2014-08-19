from django.contrib import admin

from models import Alert
from utils import get_message_handler


class AlertAdmin(admin.ModelAdmin):
    list_display = ('pk', 'level', 'tag', 'recipient', 'subject', 'is_read', 'is_email_sent', 'is_pushed', 'created')
    list_filter = ('level', 'tag')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "tag":
            kwargs['choices'] = self.tag_choices()
        return super(AlertAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def tag_choices(self):
        message_handler = get_message_handler()
        return getattr(message_handler, 'TAGS', None)

admin.site.register(Alert, AlertAdmin)

from django.contrib import admin

from models import Alert


class AlertAdmin(admin.ModelAdmin):
    list_display = ('pk', 'level', 'tag', 'recipient', 'subject', 'is_read', 'is_email_sent', 'is_pushed', 'created')
    list_filter = ('level', 'tag')

admin.site.register(Alert, AlertAdmin)

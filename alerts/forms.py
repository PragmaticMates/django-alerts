from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from models import Alert
from utils import get_message_handler


class AlertForm(ModelForm):
    tag = forms.ChoiceField(label=_(u'tag'))

    class Meta:
        model = Alert

    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        self.fields['tag'].choices = self.tag_choices()

    def tag_choices(self):
        message_handler = get_message_handler()
        return getattr(message_handler, 'TAGS', None)

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from .models import *


class RenewBookForm(forms.ModelForm):
    def clean_renewal_date(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more then 4 weeks ahead'))
        return data

    class Meta:
        model = BookInstance
        fields = ('due_back', )
        help_texts = {'due_back': _('Enter a date between now and 4 weeks'), }

from django import forms
from django.core.exceptions import ValidationError
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
import datetime
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

    def clean_content(self):
        data = self.cleaned_data['content']
        if len(data) > 500:
            raise ValidationError('Комментарий слишком длинный')
        if len(data) < 5:
            raise ValidationError('Комментарий слишком короткий')
        return data

    def save(self):
        new_com = Comment.objects.create(
            author=self.cleaned_data['author'],
            body=self.cleaned_data['body'],
            pub_date=self.cleaned_data['pub_date'],
            on_post=self.cleaned_data['on_post'],
            on_comment=self.cleaned_data['on_comment']
        )
        return new_com

from django import forms
from .widget import MultilanguageTextWidget


__all__ = ['MultilanguageFormField']


class MultilanguageFormField(forms.Field):
    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = MultilanguageTextWidget
        super().__init__(*args, **kwargs)

    def clean(self, value):
        return value

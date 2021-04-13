from django.db import models
from .model import MultilanguageText
from .form_field import MultilanguageFormField


__all__ = ['MultilanguageTextField']


class MultilanguageTextField(models.Field):
    """
        Field which provides you the way to store multilanguage text as TextField.
        The most important details:
            1. See the SEP_STRING value - it's universal separator which allows to store many languages in one string.
               You can change it if you want. But don't use simple combinations which can be found in usual texts.
            2. Note that get_internal_type method returns 'TextField'.
               It means that this field will be stored as TextField in database.
               You also can change it if you want but remember that you need more space than usual
               (texts in all languages will be concatenated including separators and language codes)
    """
    SEP_STRING = '<]|+|[>'
    description = "Field for storing text in different languages"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def dump_mlt_object(obj):
        if obj is None:
            return None
        return MultilanguageTextField.SEP_STRING.join(['{}|{}'.format(x, y) for x, y in obj.collection.items()])

    @staticmethod
    def parse_mlt_object(str_value):
        result = MultilanguageText()
        if str_value is None:
            return result
        for s in str_value.split(MultilanguageTextField.SEP_STRING):
            code, text = s.split('|', 1)
            result.set(code, text)
        return result

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.parse_mlt_object(value)

    def to_python(self, value):
        if isinstance(value, MultilanguageText):
            return value

        if value is None:
            return value

        return self.parse_mlt_object(value)

    def get_prep_value(self, value):
        return self.dump_mlt_object(value)

    def get_internal_type(self):
        return 'TextField'

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.dump_mlt_object(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': MultilanguageFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

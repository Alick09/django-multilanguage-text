from django import forms
from .model import MultilanguageText


__all__ = ['MultilanguageTextWidget']


class MultilanguageTextWidget(forms.Widget):
    """
        MultilanguageText widget.
        It's required for convenient interaction with MultilanguageTextField in some forms (like admin pages)
    """
    template_name = 'forms/widgets/multilanguage_text.html'

    def __init__(self, attrs=None):
        # Use slightly better defaults than HTML's 20x2 box
        default_attrs = {'cols': '40', 'rows': '5'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    @staticmethod
    def concat_name(name, lang):
        """ Be careful: if you change this method you also need to change template. """
        return name + '__' + lang

    def format_value(self, value):
        empty_obj = MultilanguageText()
        variants = empty_obj.get_augmented_collection()
        if isinstance(value, MultilanguageText):
            variants = value.get_augmented_collection()
        elif isinstance(value, str):
            empty_obj.set('en', value)
            variants = empty_obj.get_augmented_collection()
        elif value is not None:  # <---- is it possible ?
            variants = {'error': str(value)}

        return {'variants': variants}

    def use_required_attribute(self, initial):
        return False

    def value_from_datadict(self, data, files, name):
        languages = {lang: data.get(self.concat_name(name, lang)) for lang in MultilanguageText.get_all_languages()}
        if all(v is None or v.strip() == '' for v in languages.values()):
            return None
        return MultilanguageText(**{k: v for k, v in languages.items() if v is not None and v.strip() != ''})

    def value_omitted_from_data(self, data, files, name):
        return all(self.concat_name(name, lang) not in data for lang in MultilanguageText.get_all_languages())
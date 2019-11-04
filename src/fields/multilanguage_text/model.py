from django.utils import translation


__all__ = ['MultilanguageText']


class MultilanguageText(object):
    """
        This class presents the interface to work with multilanguage text.
        The main methods is:
            - get (you can use it as a property in html, it works awesome with i18n)
            - set (just set text for specific language)
            - is_empty (checks that object is empty)
    """
    DEFAULT_ORDER = ['en', 'ru']

    def __init__(self, **collection):
        self.collection = collection

    def get(self, language_code=None):
        if language_code is None:
            language_code = translation.get_language()
        if language_code is not None and language_code in self.collection:
            return self.collection[language_code]
        for code in self.DEFAULT_ORDER:
            if code in self.collection:
                return self.collection[code]
        return None

    def set(self, language_code, text):
        self.collection[language_code] = text

    @staticmethod
    def get_all_languages():
        return MultilanguageText.DEFAULT_ORDER

    def get_augmented_collection(self):
        """
        :return: returns full collection (with empry missed values)
        """
        res = dict([(lang, "") for lang in self.get_all_languages()])
        res.update(**self.collection)
        return res

    def is_empty(self):
        return not self.collection
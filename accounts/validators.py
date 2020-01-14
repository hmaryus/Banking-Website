import unicodedata

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

DUPLICATE_EMAIL = _(u"This email address is already in use. "
                    u"Please supply a different email address.")
DUPLICATE_USERNAME = _("A user with that username already exists.")



class CaseInsensitiveUnique(object):
    """
    Validator which performs a case-insensitive uniqueness check.
    """
    def __init__(self, model, field_name, error_message):
        self.model = model
        self.field_name = field_name
        self.error_message = error_message

    def __call__(self, value):
        # Only run if the username is a string.
        if not isinstance(value, six.text_type):
            return
        value = unicodedata.normalize('NFKC', value)
        if hasattr(value, 'casefold'):
            value = value.casefold()  # pragma: no cover
        if self.model._default_manager.filter(**{
                '{}__iexact'.format(self.field_name): value
        }).exists():
            raise ValidationError(self.error_message, code='unique')


def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    if exists:
        raise ValidationError("Email address %s already exists, must be unique" % value)


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = 0

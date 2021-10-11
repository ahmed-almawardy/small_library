from  django.core import validators
from django.conf import settings


name_no_numbers_symbols = validators.RegexValidator(
    regex = settings.NAME_ONLY_CHARS_DASH_UNDERSOCER,
    message='Name can contain only (letters - or _ )'
)

phone_with_plus = validators.RegexValidator(
    regex = settings.PHONE_VALIDATOR,
    message="phone only from 11 to 20 numbers with no letters (+) allowed "
)
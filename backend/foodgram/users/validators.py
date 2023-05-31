import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def check_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Имя пользователя не может быть "Me, ME, me, mE'
        )


def check_name(value):
    if not re.match(r'^[A-Za-zА-Яа-я]+$', value):
        raise ValidationError(
            _('допускаются только буквы'),
            code='недопустимое имя'
        )

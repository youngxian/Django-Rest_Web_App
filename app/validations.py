from django.core.exceptions import ValidationError
from app import messages

def validate_password(password):
    ''' 
    Validate Password 
    '''

    if password is None:
        raise ValidationError(messages.MANDATORY_DETAILS_REQUIRED,
                              code='required', params={'password': 'password'})
    elif len(password) < 6:
        raise ValidationError(messages.INVALID_PASSWORD_LENGTH,
                              code='min_length', params={'password': 'password'})
    elif password.isdigit() or not any(char.isdigit() for char in password):
        raise ValidationError(
            messages.ALPHANUMERIC_PASSWORD_REQUIRED,
            code='alphanumeric_password', params={'password': 'password'}
        )
    else:
        return password
from rest_framework.exceptions import ValidationError


def validate_phone_length(data):
    if len(str(data)) != 11:
        raise ValidationError("Номер должен состоять из 11 цифр.")
    return data
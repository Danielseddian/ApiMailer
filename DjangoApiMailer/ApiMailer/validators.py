from rest_framework.exceptions import ValidationError


def validate_phone(data):
    try:
        if int(data) not in range(7*10**10, 8*10**10):
            raise ValueError()
    except (ValueError, TypeError):
        raise ValidationError("Номер должен состоять из 11 цифр, начиная с 7.")
    return data
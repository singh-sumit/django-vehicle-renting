from django.core.exceptions import ValidationError
from django.utils import timezone


###################################################
#               validte phone number
import re


def validate_phone(phone):
    if phone.isnumeric():
        # pattern : 9812345678
        regex_string = r"(\+977 )?" + "9(8|7)" + r"\d" * 8
        phone_regex = re.compile(regex_string)
        is_valid = phone_regex.fullmatch(phone)
        if not is_valid:
            raise ValidationError("Enter a proper mobile number.")
    else:
        raise ValidationError("Phone number must be numeric")

#####################################################################
#                   Calculate age given two dates
def age(dob):
    today = timezone.now().date()
    if (today.month < dob.month) or \
            (today.month == dob.month and today.day < dob.day):
        return today.year - dob.year - 1
    else:
        return today.year - dob.year

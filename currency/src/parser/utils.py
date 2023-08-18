import re


def validate_date(value):
    date_pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{4}')
    if not date_pattern.match(value):
        raise ValueError("Invalid date format. Please use the format dd/mm/yyyy")
    day, month, year = map(int, value.split('/'))
    if not (1 <= day <= 31 and 1 <= month <= 12):
        raise ValueError("Invalid day or month values")
    return value

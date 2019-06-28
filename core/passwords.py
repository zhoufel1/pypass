import string
import random

UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase


def generate_password(length: int) -> str:
    return ''.join([determine_type(random.randint(0, 2))
                   for i in range(length)])


def determine_type(value: int) -> str:
    if value == 0:
        return LOWER[random.SystemRandom().randint(0, 25)]
    elif value == 1:
        return UPPER[random.SystemRandom().randint(0, 25)]
    else:
        return str(random.SystemRandom().randint(0, 9))

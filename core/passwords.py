import string
import random

UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase


def generate_password(length: int) -> str:
    password = ''
    index = 0
    while index < length:
        character_type = random.randint(0, 2)
        if character_type == 0:
            password += LOWER[random.SystemRandom().randint(0, 25)]
        elif character_type == 1:
            password += UPPER[random.SystemRandom().randint(0, 25)]
        else:
            password += str(random.SystemRandom().randint(0, 9))
        index += 1
    return password

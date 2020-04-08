import string
from random import SystemRandom

LETTERS = string.ascii_letters
DIGITS = string.digits

def generate_password(length: int) -> str:
    password_array = []
    for _ in range(length):
        if SystemRandom().randint(0, 1):
            password_array.append(LETTERS[SystemRandom().randint(0, len(LETTERS) - 1)])
        else:
            password_array.append(DIGITS[SystemRandom().randint(0, len(DIGITS) - 1)])
    return ''.join(password_array)

#!/usr/bin/env python3
# Password generator class
import string

from random import randint


class Passgen():
    """A password generator"""
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase

    def __init__(self, length: int):
        """Initialize the password generator"""
        self.length = length

    def gen_upper_xor_lower(self, caps: bool):
        """Returns a string representing a password that is all capitalized if caps is True and all 
        lowercase if Caps is False."""
        passw = ""
        for i in range(self.length):
            if not caps:
                passw += self.lower[randint(0, 25)]
            else:
                passw += self.upper[randint(0, 25)]
        return passw

    def gen_upper_and_lower(self):
        """Return a string representing a password that includes lower and uppercase alpha characters"""
        passw = ""
        for i in range(self.length):
            ran = randint(0, 1)
            if ran == 0:
                passw += self.lower[randint(0, 25)]
            else:
                passw += self.upper[randint(0, 25)]
        return passw

    def gen_password(self):
        """Return a string representing a password containing characters that are alphanumeric upper and lowercase."""
        passw = ""
        for i in range(self.length):
            ran = randint(0, 2)
            if ran == 0:
                passw += self.lower[randint(0, 25)]
            elif ran == 1:
                passw += self.upper[randint(0, 25)]
            else:
                passw += str(randint(0, 9))
        return passw

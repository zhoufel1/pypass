#!/usr/bin/env python3
import string

from random import randint


class Passgen():
    """A password generator"""
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase

    def __init__(self, length: int) -> None:
        """Initialize the password generator"""
        self.length = length

    def gen_upper_xor_lower(self, caps: bool) -> str:
        """Returns a string representing a password that is all capitalized if
        caps is True and all lowercase if Caps is False."""
        passw = ""
        i = 0
        while i < self.length:
            if not caps:
                passw += self.lower[randint(0, 25)]
            else:
                passw += self.upper[randint(0, 25)]
            i += 1
        return passw

    def gen_upper_and_lower(self) -> str:
        """Return a string representing a password that includes
        lower and uppercase alpha characters"""
        passw = ""
        i = 0
        while i < self.length:
            ran = randint(0, 1)
            if ran == 0:
                passw += self.lower[randint(0, 25)]
            else:
                passw += self.upper[randint(0, 25)]
            i += 1
        return passw

    def gen_password(self) -> str:
        """Return a string representing a password containing characters
        that are alphanumeric upper and lowercase."""
        passw = ""
        i = 0
        while i < self.length:
            ran = randint(0, 2)
            if ran == 0:
                passw += self.lower[randint(0, 25)]
            elif ran == 1:
                passw += self.upper[randint(0, 25)]
            else:
                passw += str(randint(0, 9))
            i += 1
        return passw

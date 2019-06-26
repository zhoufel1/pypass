#!/usr/bin/env python3

from __future__ import annotations
from typing import Callable, Optional
import os
import tty
import sys
import termios


class Getch:
    """A class to retrieve a single character from standard input."""

    def __call__(self) -> None:
        file_desc = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_desc)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)
        return char


class MenuObject:
    """A base class to represent objects inside a menu."""

    def __init__(self, title: str) -> None:
        """Initialize the MenuObject object given the <title>."""
        self.title = title
        self.selected = False

    def __repr__(self) -> str:
        """Return a string representation of the MenuObject."""
        if self.selected:
            return f'> {self.title}'
        return f'  {self.title}'


class Option(MenuObject):
    """An option in a menu that a user can select."""

    def __init__(self, title: str, func: Callable) -> None:
        """Initialize the option object."""
        super().__init__(title)
        self.func = func


class Menu(MenuObject):
    """A menu that a user can interact with. A menu can exist
    as a submenu of another parent menu."""

    def __init__(self, title: str, parent: Optional[Menu] = None):
        """Initialize an empty menu object. If <parent> is None,
        then the menu is base menu. Otherwise, it is a submenu
        to <parent>."""
        super().__init__(title)
        self.parent = parent
        self.options = []
        self.pointer = None

    def add_option(self, option: MenuObject) -> None:
        """Add the <option> to the menu. If the menu is
        currently empty, select <option> and point to it."""
        if not self.options:
            self.pointer = option
            self.pointer.selected = True
        self.options.append(option)

    def print_options(self) -> None:
        """Print the items in the menu."""
        for item in self.options:
            print(item)

    def point_next(self) -> None:
        """Point to the next option in the menu if it exists.
        Otherewise, do nothing."""
        if self.options.index(self.pointer) + 1 == len(self.options):
            return None
        else:
            self.pointer.selected = False
            self.pointer = self.options[self.options.index(self.pointer) + 1]
            self.pointer.selected = True

    def point_prev(self) -> None:
        """Point to the previous option in the menu if it exists.
        Otherwise, do nothing."""
        if self.options.index(self.pointer) - 1 < 0:
            return None
        else:
            self.pointer.selected = False
            self.pointer = self.options[self.options.index(self.pointer) - 1]
            self.pointer.selected = True

#!/usr/bin/env python3
from __future__ import annotations
from typing import Callable, Optional


class MenuObject:
    def __init__(self, title: str) -> None:
        self.title = title
        self.selected = False

    def __repr__(self) -> str:
        if self.selected:
            return f'❭ {self.title}'
        return f'  {self.title}'


class Option(MenuObject):
    def __init__(self, title: str, func: Callable) -> None:
        super().__init__(title)
        self.func = func


class Menu(MenuObject):
    def __init__(self, title: str, parent: Optional[Menu] = None):
        super().__init__(title)
        self.parent = parent
        self.options = []
        self.pointer = None

    def add_option(self, option: MenuObject) -> None:
        if not self.options:
            self.pointer = option
            self.pointer.selected = True
        self.options.append(option)

    def print_options(self) -> None:
        for item in self.options:
            print(item)

    def point_next(self) -> None:
        if self.options.index(self.pointer) + 1 == len(self.options):
            return None
        else:
            self.pointer.selected = False
            self.pointer = self.options[self.options.index(self.pointer) + 1]
            self.pointer.selected = True

    def point_prev(self) -> None:
        if self.options.index(self.pointer) - 1 < 0:
            return None
        else:
            self.pointer.selected = False
            self.pointer = self.options[self.options.index(self.pointer) - 1]
            self.pointer.selected = True

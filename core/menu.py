#!/usr/bin/env python3

from __future__ import annotations
from typing import Callable, Optional
import data_manipulation as data_manip


class MenuObject:

    def __init__(self, title: str) -> None:
        self.title = title
        self.selected = False

    def __repr__(self) -> str:
        if self.selected:
            return f'> {self.title}'
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


def build_main_menu() -> Menu:
    base_menu = Menu(None)
    base_menu.add_option(build_search_menu(base_menu))
    base_menu.add_option(build_input_menu(base_menu))
    base_menu.add_option(Option("Update existing entry",
                         data_manip.update_data))
    base_menu.add_option(Option('Delete existing entry',
                         data_manip.delete_data))
    base_menu.add_option(Option('Reset database', data_manip.delete_all))
    return base_menu


def build_search_menu(base_menu: Menu) -> Menu:
    search_menu = Menu('Show entries', base_menu)
    search_menu.add_option(Option('Search', data_manip.show_search))
    search_menu.add_option(Option('Show all', data_manip.show_all))
    return search_menu


def build_input_menu(base_menu: Menu) -> Menu:
    input_menu = Menu('Add new entry', base_menu)
    input_menu.add_option(Option('Generate password', data_manip.input_data))
    input_menu.add_option(Option('Enter existing password',
                          data_manip.input_existing_data))
    return input_menu

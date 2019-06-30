#!/usr/bin/env python3

import os
import menu
import data_manipulation as dm
import pyperclip as clip
import database as db
import encryption as enc
from typing import Optional
from constants import ENTER, UP, DOWN, LEFT


class PasswordError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def run() -> None:
    database = db.Database()

    os.system('clear')
    print("━━━━━━━━━━━Password Manager━━━━━━━━━━━")

    trigger = dm.create_database(database)
    key = enc.key_generator(dm.handle_password(trigger, database))

    main_menu = menu.build_main_menu()
    menu_loop(main_menu, database, key)


def menu_loop(main_menu: menu.Menu,
              database: db.Database, key: bytes) -> Optional[int]:
    os.system('tput civis')

    while True:
        os.system('clear')
        main_menu.print_options()
        user_input = get_user_input()
        if user_input == 'k' or user_input == UP:
            main_menu.point_prev()
        elif user_input == 'j' or user_input == DOWN:
            main_menu.point_next()
        elif user_input == 'l' or user_input == ENTER:
            if isinstance(main_menu.pointer, menu.Menu):
                menu_loop(main_menu.pointer, database, key)
                break
            elif isinstance(main_menu.pointer, menu.Option):
                os.system('clear')
                if main_menu.pointer.func == dm.show_all:
                    main_menu.pointer.func(database, key)
                    input("\nPress Enter to continue...")
                elif main_menu.pointer.func.__code__.co_argcount \
                        == 2:
                    main_menu.pointer.func(database, key)
                else:
                    main_menu.pointer.func(database)
        elif user_input == 'h' or user_input == LEFT:
            if main_menu.parent is not None:
                menu_loop(main_menu.parent, database, key)
                break
        elif user_input == 'q':
            os.system('clear')
            os.system('tput cnorm')
            clip.copy('')
            return None


def get_user_input() -> str:
    from getch import Getch
    getch = Getch()
    char = getch()
    if char == '\x1b':
        getch()
        return '\\' + getch()
    return char


if __name__ == '__main__':
    run()

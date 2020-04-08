#!/usr/bin/env python3
import data_logic
import encryption
import pyperclip
from menu import Menu, Option
from system import clear_screen, hide_cursor, show_cursor, getch
from database import AccountDatabase
from constants import ENTER, BACKSPC, ESC, UP, DOWN, LEFT

def menu_loop(menu: Menu, database: AccountDatabase=None, key: bytes=None):
    hide_cursor()
    while True:
        clear_screen()
        menu.print_options()
        user_input = getch()
        if user_input == 'k' or user_input == UP:
            menu.point_prev()
        elif user_input == 'j' or user_input == DOWN:
            menu.point_next()
        elif user_input == 'l' or user_input == ENTER:
            if isinstance(menu.pointer, Menu):
                menu_loop(menu.pointer , database, key)
                break
            else:
                if menu.pointer.func.__code__.co_argcount == 2:
                    menu.pointer.func(database, key)
                elif menu.pointer.func.__code__.co_argcount == 1:
                    menu.pointer.func(database)
                else:
                    menu.pointer.func()

        elif user_input == 'q':
            show_cursor()
            return 0

# Main Menu
def build_main_menu() -> Menu:
    main_menu = Menu(None)
    main_menu.add_option(Option("Search Passwords", temp))
    main_menu.add_option(Option("Show All Accounts", temp))
    main_menu.add_option(Option("Show Help", show_help))
    main_menu.add_option(Option("Reset Database", reset_database_flow))
    return main_menu


# Help Flow
def show_help() -> None:
    clear_screen()
    print(
            "TEST"
            )
    getch()
    return None

# Reset Database Flow
def reset_database_flow(database: AccountDatabase) -> None:
    import bcrypt
    import getpass
    import time
    clear_screen()
    password = getpass.getpass("You are about to delete account info. " +
                          "This is irreversible.\n\n" +
                          "Enter your master password to confirm []: ")
    if not bcrypt.checkpw(password.encode(), database.retrieve_password()):
        print("[Error]: Password incorrect. Aborted")
        time.sleep(1.3)
    else:
        database.drop_tables()
        print("All account information deleted")
        input("\nPress Enter to continue...")


# Update Password Flow
def build_update_menu() -> Menu:
    update_menu = Menu(None)
    update_menu.add_option(Option("Generate New Password", update_password_flow))
    update_menu.add_option(Option("Enter Existing Password", temp))
    return update_menu

def update_password_flow(database: AccountDatabase, key: bytes) -> None:
    from password_generator import generate_password

    is_invalid = False
    while True:
        clear_screen()

        title_string = "Generating Password"
        if is_invalid:
            title_string += "    INVALID INPUT"
        title_string += "\n"
        print(title_string)

        length = input("Specify length []: ")
        if length.isnumeric():
            break
        is_invalid = True

    new_password = generate_password(int(length))


def temp():
    pass

if __name__ == "__main__":
    menu_loop(build_main_menu())

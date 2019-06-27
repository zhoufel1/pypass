#!/usr/bin/env python3

import os
import time
import passwords
import getpass as gp
import database as db
import encryption as enc
import bcrypt
import search
import menu
import pyperclip as pyper
from typing import Optional


class PasswordError(Exception):
    """An exception that should be raised if the
    inputted password is incorrect."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""

        super().__init__(message)


def run() -> None:
    """Initialize the program"""

    database = db.Database()

    os.system('clear')
    print("━━━━━━━━━━━Password Manager━━━━━━━━━━━")

    trigger = create_database(database)
    key = enc.key_generator(handle_password(trigger, database))

    main_menu = build_main_menu()
    menu_loop(main_menu, database, key)


def build_main_menu() -> menu.Menu:
    """Return a menu.Menu containing the menu tree for the program."""
    base_menu = menu.Menu(None)
    base_menu.add_option(build_search_menu(base_menu))
    base_menu.add_option(build_input_menu(base_menu))
    base_menu.add_option(menu.Option("Update existing entry",
                         update_data))
    base_menu.add_option(menu.Option('Delete existing entry',
                         delete_data))
    base_menu.add_option(menu.Option('Reset database', delete_all))
    return base_menu


def build_search_menu(base_menu: menu.Menu) -> menu.Menu:
    """Return a menu.Menu containing the options for the
    search branch of the menu tree."""
    search_menu = menu.Menu('Show entries', base_menu)
    search_menu.add_option(menu.Option('Search', show_search))
    search_menu.add_option(menu.Option('Show all', show_all))
    return search_menu


def build_input_menu(base_menu: menu.Menu) -> menu.Menu:
    """Return a menu.Menu containing the options for the
    input branch of the menu tree."""
    input_menu = menu.Menu('Add new entry', base_menu)
    input_menu.add_option(menu.Option('Generate password', input_data))
    input_menu.add_option(menu.Option('Enter existing password',
                          input_existing_data))
    return input_menu


def menu_loop(main_menu: menu.Menu,
              database: db.Database, key: bytes) -> Optional[int]:
    """The loop for the main menu of the program."""
    os.system('tput civis')

    while True:
        os.system('clear')
        main_menu.print_options()
        user_input = get_user_input()
        if user_input == 'k' or user_input == '\\A':
            main_menu.point_prev()
        elif user_input == 'j' or user_input == '\\B':
            main_menu.point_next()
        elif user_input == 'l' or user_input == '\r':
            if isinstance(main_menu.pointer, menu.Menu):
                menu_loop(main_menu.pointer, database, key)
                break
            elif isinstance(main_menu.pointer, menu.Option):
                os.system('clear')
                if main_menu.pointer.func == show_all:
                    main_menu.pointer.func(database, key)
                    input("Press Enter to continue...")
                elif main_menu.pointer.func.__code__.co_argcount \
                        == 2:
                    main_menu.pointer.func(database, key)
                else:
                    main_menu.pointer.func(database)
        elif user_input == 'h' or user_input == '\\D':
            if main_menu.parent is not None:
                menu_loop(main_menu.parent, database, key)
                break
        elif user_input == 'q':
            os.system('clear')
            os.system('tput cnorm')
            pyper.copy('')
            return None


def get_user_input() -> str:
    """Return a string representing the next character input,
    checking for arrow key inputs."""
    getch = menu.Getch()
    char = getch()
    if char == '\x1b':
        getch()
        return '\\' + getch()
    return char


def create_database(database: db.Database) -> bool:
    """Return True if the database already exist. If not, create the database
    and return False"""

    if not os.path.exists('./account_database.db'):
        print("Creating account database...")
        database.create_database()
        return False
    print("Accessing database...")
    return True


def handle_password(trigger: bool, database: db.Database) -> str:
    """Return the user-inputted password as a string. If database is
    already created, check the inputted password with database password.
    Otherwise, prompt user to create a password for the database"""

    if trigger:
        entry = gp.getpass("Enter your password: ")
        if not bcrypt.checkpw(entry.encode(),
                              database.retrieve_password()):
            raise Exception("Incorrect password")
        return entry

    while True:
        first_entry = gp.getpass("Enter a password for database: ")
        second_entry = gp.getpass("Re-enter the password: ")
        if first_entry == second_entry:
            database.set_password(enc.hash_password(first_entry))
            return first_entry

        os.system('clear')
        print("*Passwords do not match*")
        time.sleep(1)
        os.system('clear')


def show_search(database: db.Database, key: bytes) -> None:
    """Prompt the user to enter a search query and print all
    account information associated with that site. If multiple
    queries are found, have the user select."""

    os.system('tput cnorm')
    if check_database_empty(database):
        os.system('tput civis')
        return None
    else:
        search_result = user_enter_query(database)
        if search_result == '\x1b':
            return None
        results = fuzzy_search(search_result, database)
        op = build_menu_options(results)
        if len(op) == 1:
            pyper.copy(enc.decrypt_password(op[1].password, key))
        else:
            while True:
                u_input = input("Enter option: ").strip()
                if u_input.isnumeric() and int(u_input) <= len(op):
                    pw = enc.decrypt_password(op[int(u_input)].password, key)
                    pyper.copy(pw)
                    break
        os.system('clear')
        print("Password copied")
        time.sleep(1)
        os.system('clear')
        os.system('tput civis')


def show_all(database: db.Database, key: bytes) -> None:
    """Print all account information in the database"""

    queries = database.query_all_entries()
    if not queries:
        print("No items found\n")
    else:
        print("\n━━━━━━━━━━━━Account Info━━━━━━━━━━━━")
        for site in queries:
            print("*** " + site + ":")
            for item in queries[site]:
                print(item.username, enc.decrypt_password(item.password, key))
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


def input_data(database: db.Database, key: bytes) -> None:
    """Prompts the user to enter account information and store it into the
    Account table in database as a row"""

    os.system('tput cnorm')
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")

    if database.query_site_and_user(site, username) != {}:
        os.system('clear')
        print("*Item already exists*")
        time.sleep(1)
    else:
        while True:
            length = input("Password length? ")
            if length.isnumeric():
                password = passwords.generate_password(int(length))
                database.insert_data(site,
                                     username,
                                     enc.encrypt_password(password,
                                                          key))
                pyper.copy(password)
                os.system('clear')
                print("Password copied!")
                time.sleep(1)
                os.system('tput civis')
                return None


def input_existing_data(database: db.Database, key: bytes) -> None:
    """Prompts the user to enter account information and password
    and store it int the Account table in database as a row."""

    os.system('tput cnorm')
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")
    password = input("Enter password: ")

    if database.query_site_and_user(site, username) != {}:
        os.system('clear')
        print("*Item already exists*")
        time.sleep(1)
    else:
        database.insert_data(site,
                             username,
                             enc.encrypt_password(password, key))
        os.system('clear')
        print("Account information stored")
        time.sleep(1)
    os.system('tput civis')


def update_data(database: db.Database, key: bytes) -> None:
    """Prompts the user to enter account information to update that row
    with a new generated password"""

    os.system('tput cnorm')
    if check_database_empty(database):
        return None
    else:
        search_result = user_enter_query(database)
        if search_result == '\x1b':
            return None
        results = fuzzy_search(search_result, database)
        op = build_menu_options(results)
        if len(op) == 1:
            selection = op[1]
        else:
            while True:
                u_input = input("Enter option: ").strip()
                if u_input.isnumeric() and int(u_input) <= len(op):
                    selection = op[int(u_input)]
                    break
        password = passwords.generate_password(int(input("Length? ")))
        new_password = enc.encrypt_password(password, key)
        database.update_item(selection.site,
                             selection.username,
                             new_password)
        os.system('clear')
        print("Password copied")
        time.sleep(1)
        os.system('clear')
        os.system('tput civis')


def delete_data(database: db.Database) -> None:
    """Handles row deletion"""

    os.system('tput cnorm')
    if check_database_empty(database):
        return None
    else:
        search_result = user_enter_query(database)
        if search_result == '\x1b':
            return None
        results = fuzzy_search(search_result, database)
        op = build_menu_options(results)
        if len(op) == 1:
            selection = op[1]
        else:
            while True:
                u_input = input("Enter option: ").strip()
                if u_input.isnumeric() and int(u_input) <= len(op):
                    selection = op[int(u_input)]
                    break
        os.system('clear')
        database.delete_row(selection.site,
                            selection.username)
        print("Account info deleted")
        time.sleep(1)
        os.system('clear')
        os.system('tput civis')


def delete_all(database: db.Database) -> None:
    """Handles table deletion"""
    password = gp.getpass("You are about to wipe account info. " +
                          "Enter password to confirm: ")
    os.system('clear')
    if not bcrypt.checkpw(password.encode(),
                          database.retrieve_password()):
        print("*Password incorrect. Aborted*")
        time.sleep(1)
    else:
        database.drop_tables()
        print("All account information deleted")
        input("\nPress Enter to continue...")


# ======================Search Menu Logic========================
def user_enter_query(database: db.Database) -> str:
    """"""
    os.system('tput civis')
    user_search = ''
    while True:
        os.system('clear')
        print("Enter search: " + user_search)
        results = fuzzy_search(user_search, database)
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if not results:
            print('None exist')
        else:
            project_menu(build_menu_options(results))
        user_input = menu.Getch()()
        if user_input == '\r' and results != []:
            break
        elif user_input == '\r' and results == []:
            continue
        elif user_input == '\x7f' and user_search == '':
            pass
        elif user_input == '\x7f' and user_search != '':
            user_search = user_search[:-1]
        elif user_input == '\x1b':
            return '\x1b'
        elif user_input.isprintable():
            user_search += user_input.lower()
    return user_search


def invoke_menu(input_list: list):
    """
    Display the meny of options and prompt the user to select a
    valid option. Retrieve the password with the associated selection.

    """
    options = build_menu_options(input_list)
    if not options:
        print("No items found")
        time.sleep(1)
        os.system('clear')
    project_menu(options)
    print('\n')
    while True:
        user_input = input("Enter option: ").strip()
        if user_input.isnumeric() and int(user_input) <= len(options):
            return options[int(user_input)]


def project_menu(menu_options: dict) -> None:
    """
    Show the options in the menu_options.
    """
    for item in menu_options:
        print('[' + str(item) + ']' + ' Site: ' + menu_options[item].site +
              '\n    User: ' + menu_options[item].username)


def build_menu_options(input_list: list) -> list:
    """Return a dictionary wherein the keys
    correspond to integer input values starting from 0
    the values are the account information."""

    results = {}
    for i in range(len(input_list)):
        results[i + 1] = input_list[i]
    return results


def check_database_empty(database: db.Database) -> bool:
    """Return True if <database> is empty, that is it has no
    entries. Otherwise, return False.
    """
    if database.is_empty():
        print("Database is empty...")
        input("\nPress Enter to continue...")
        os.system('clear')
        return True
    return False


def fuzzy_search(search_input: str, database: db.Database) -> list:
    """
    Prompt the user for a query and return a list containing items
    that the fuzzy search yields.
    """

    if not search_input:
        results = database.query_database()
    else:
        results = [item for item in database.query_database()
                   if search.is_found(search_input, item.site)
                   or search.is_found(search_input, item.username)]
    return results


if __name__ == '__main__':
    run()

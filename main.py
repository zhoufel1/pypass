#!/usr/bin/env python3

import os
import pyperclip
import time
from getpass import getpass
import database_handler as db
from encryption import (
        key_generator,
        encrypt_password,
        decrypt_password,
        hash_password
        )
from passgen import Passgen
from bcrypt import checkpw
from searching import is_found


class PasswordError(Exception):
    """An exception that should be raised if the
    inputted password is incorrect."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""

        super().__init__(message)


def run() -> None:
    """Initialize the program"""

    # Create database handler object
    database_handler = db.DatabaseHandler()

    os.system('clear')
    print("======================Password" +
          "Manager======================")

    # Handle password entry
    trigger = create_database(database_handler)
    key = key_generator(handle_password(trigger, database_handler))

    # Initialize menu options
    os.system('clear')
    user_input = input("\nOptions:\n" +
                       "[1] Show entries\n" +
                       "[2] Add new entry\n" +
                       "[3] Update existing entry\n" +
                       "[4] Delete existing entry\n" +
                       "[5] Reset database\n" +
                       "[6] Exit\n")

    # Menu loop
    while True:
        os.system('clear')
        if user_input == "1":
            os.system('clear')
            search_input = input("\nOptions:\n" +
                                 "[1] Search\n" +
                                 "[2] Show all\n")
            os.system('clear')
            if search_input == '1':
                show_search_query(database_handler, key)
            elif search_input == '2':
                show_all_data(database_handler, key)
        elif user_input == "2":
            handle_data_input(database_handler, key)
        elif user_input == "3":
            handle_data_update(database_handler, key)
        elif user_input == "4":
            handle_data_delete(database_handler)
        elif user_input == "5":
            confirm = input("Are your sure? (Y/n)\n")
            if confirm == 'Y':
                handle_table_delete(database_handler)
        elif user_input == "6":
            pyperclip.copy('')
            return 0
        user_input = input("\nOptions:\n" +
                           "[1] Show entries\n" +
                           "[2] Add new entry\n" +
                           "[3] Update existing entry\n" +
                           "[4] Delete existing entry\n" +
                           "[5] Reset database\n" +
                           "[6] Exit\n")


def create_database(database_handler) -> bool:
    """Return True if the database already exist. If not, create the database
    and return False"""

    if not os.path.exists('./account_database.db'):
        print("Creating account database...")
        database_handler.create_database()
        return False
    print("Accessing database...")
    return True


def handle_password(trigger: bool, database_handler) -> str:
    """Return the user-inputted password as a string. If database is
    already created, check the inputted password with database password.
    Otherwise, prompt user to create a password for the database"""

    if trigger:
        p_input = getpass("Enter your password: ")
        if not checkpw(p_input.encode(), database_handler.retrieve_password()):
            raise Exception("Incorrect password")
        return p_input
    else:
        while True:
            first_entry = getpass("Enter a password for database: ")
            second_entry = getpass("Re-enter the password: ")
            if first_entry == second_entry:
                database_handler.set_password(hash_password(p_input))
                return p_input
            print("*Passwords do not match*")


def show_search_query(database_handler, key: bytes) -> None:
    """Prompt the user to enter a search query and print all
    account information associated with that site. If multiple
    queries are found, have the user select."""

    if database_handler.is_empty():
        print("Database is empty...")
        time.sleep(1)
        os.system('clear')
    else:
        search_input = input("\nEnter search: ").lower().strip(" ")
        queries = database_handler.query_database()
        results = []
        for item in queries:
            if is_found(search_input, item.site) or \
                    is_found(search_input, item.username):
                results.append(item)
        os.system('clear')
        if results == []:
            os.system('clear')
            print('No results found')
            time.sleep(1)
            os.system('clear')
        else:
            pyperclip.\
                copy(decrypt_password(invoke_menu(results).password, key))
            os.system('clear')
            print("Password copied")
            time.sleep(1)
            os.system('clear')


def show_all_data(database_handler, key: bytes) -> None:
    """Print all account information in the database"""
    queries = database_handler.query_all_entries()
    print("\n============Account Info============")
    for site in queries:
        print("*** " + site + ":")
        for item in queries[site]:
            print(item.username, decrypt_password(item.password, key))
    print("====================================")


def handle_data_input(database_handler, key: bytes) -> None:
    """Prompts the user to enter account information and store it into the
    Account table in database as a row"""
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")
    if database_handler.query_site_and_user(site, username) != {}:
        print("*Item already exists*")
    else:
        try:
            length = input("Password length? ")
            password = Passgen(int(length)).gen_password()
            database_handler.insert_data(site, username,
                                         encrypt_password(password, key))
            pyperclip.copy(password)
            print("Password copied!")
        except ValueError:
            print("Invalid entry")


def handle_data_update(database_handler, key: bytes) -> None:
    """Prompts the user to enter account information to update that row
    with a new generated password"""
    if database_handler.is_empty():
        print("Database is empty...")
        time.sleep(1)
        os.system('clear')
    else:
        search_input = input("\nEnter search: ").lower().strip(" ")
        queries = database_handler.query_database()
        results = []
        for item in queries:
            if is_found(search_input, item.site) or \
                    is_found(search_input, item.username):
                results.append(item)
        os.system('clear')
        if results == []:
            print("No results found")
            time.sleep(1)
            os.system('clear')
        else:
            selec = invoke_menu(results)
            password = Passgen(int(input("Length? "))).gen_password()
            new_password = encrypt_password(password, key)
            database_handler.\
                update_item(selec.site, selec.username, new_password)
            os.system('clear')
            pyperclip.copy(password)
            print("Password copied!")


def handle_data_delete(database_handler) -> None:
    """Handles row deletion"""
    if database_handler.is_empty():
        print("Database is empty...")
        time.sleep(1)
        os.system('clear')
    else:
        search_input = input("\nEnter search: ").lower().strip(" ")
        queries = database_handler.query_database()
        results = []
        for item in queries:
            if is_found(search_input, item.site) or \
                    is_found(search_input, item.username):
                results.append(item)
        os.system('clear')
        if results == []:
            print("No results found")
            time.sleep(1)
            os.system('clear')
        else:
            selec = invoke_menu(results)
            os.system('clear')
            print("Account info deleted")
            database_handler.delete_row(selec.site, selec.username)
            time.sleep(1)
            os.system('clear')

def handle_table_delete(database_handler) -> None:
    """Handles table deletion"""
    password = getpass("You are about to wipe account info. " +
                       "Enter password to confirm: ")
    if not checkpw(password.encode(), database_handler.retrieve_password()):
        print("*Password incorrect. Aborted*")
    else:
        print("Dropping table...")
        database_handler.drop_tables()


# ======================Search Menu Logic========================

def invoke_menu(input_list: list) -> None:
    """
    Display the meny of options and prompt the user
    to select a valid option. Retrieve the password
    with the associated selection.

    """
    options = build_menu_options(input_list)
    if options == {}:
        print("No items found")
        time.sleep(0.5)
        os.system('clear')
    show_menu(options)
    print('\n')
    user_input = input("Which account? ").strip()
    while not user_input.isnumeric():
        user_input = input("Enter valid input: ").strip()
    return options[int(user_input)]


def show_menu(menu_options: dict) -> None:
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


if __name__ == '__main__':
    run()

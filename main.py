#!/usr/bin/env python3

import os
import pyperclip
import time
import passwords
import getpass as gp
import database as db
import encryption as enc
import bcrypt
import searching


class PasswordError(Exception):
    """An exception that should be raised if the
    inputted password is incorrect."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""

        super().__init__(message)


def run() -> None:
    """Initialize the program"""

    # Create database handler object
    database = db.Database()

    os.system('clear')
    print("======================Password" +
          "Manager======================")

    # Handle password entry
    trigger = create_database(database)
    key = enc.key_generator(handle_password(trigger, database))

    # Menu loop
    while True:
        os.system('clear')
        user_input = input("[1] Show entries\n" +
                           "[2] Add new entry\n" +
                           "[3] Update existing entry\n" +
                           "[4] Delete existing entry\n" +
                           "[5] Reset database\n" +
                           "[6] Exit\n")
        os.system('clear')
        if user_input == "1":
            search_input = input("[1] Search\n" +
                                 "[2] Show all\n")
            os.system('clear')
            if search_input == '1':
                show_search_query(database, key)
            elif search_input == '2':
                show_all_data(database, key)
                input("Press Enter to continue...")
        elif user_input == "2":
            handle_data_input(database, key)
        elif user_input == "3":
            handle_data_update(database, key)
        elif user_input == "4":
            handle_data_delete(database)
        elif user_input == "5":
            confirm = input("Are your sure? (Y/n)\n")
            if confirm == 'Y':
                os.system('clear')
                handle_table_delete(database)
        elif user_input == "6":
            pyperclip.copy('')
            return 0


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


def show_search_query(database: db.Database, key: bytes) -> None:
    """Prompt the user to enter a search query and print all
    account information associated with that site. If multiple
    queries are found, have the user select."""

    if check_database_empty(database):
        return None
    else:
        results = fuzzy_search(database)
        if not results:
            return None
        else:
            pyperclip.\
                copy(enc.decrypt_password(invoke_menu(results).password, key))
            os.system('clear')
            print("Password copied")
            time.sleep(1)
            os.system('clear')


def show_all_data(database: db.Database, key: bytes) -> None:
    """Print all account information in the database"""

    queries = database.query_all_entries()
    print("\n============Account Info============")
    for site in queries:
        print("*** " + site + ":")
        for item in queries[site]:
            print(item.username, enc.decrypt_password(item.password, key))
    print("====================================")


def handle_data_input(database: db.Database, key: bytes) -> None:
    """Prompts the user to enter account information and store it into the
    Account table in database as a row"""

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
                pyperclip.copy(password)
                os.system('clear')
                print("Password copied!")
                time.sleep(1)
                return None


def handle_data_update(database: db.Database, key: bytes) -> None:
    """Prompts the user to enter account information to update that row
    with a new generated password"""

    if check_database_empty(database):
        return None
    else:
        results = fuzzy_search(database)
        if not results:
            return None
        else:
            selection = invoke_menu(results)
            password = passwords.generate_password(int(input("Length? ")))
            new_password = enc.encrypt_password(password, key)
            database.update_item(selection.site,
                                 selection.username,
                                 new_password)
            os.system('clear')
            pyperclip.copy(password)
            print("Password copied!")
            time.sleep(1)


def handle_data_delete(database: db.Database) -> None:
    """Handles row deletion"""

    if check_database_empty(database):
        return None
    else:
        results = fuzzy_search(database)
        if not results:
            return None
        else:
            selection = invoke_menu(results)
            os.system('clear')
            print("Account info deleted")
            database.delete_row(selection.site,
                                        selection.username)
            time.sleep(1)
            os.system('clear')


def handle_table_delete(database: db.Database) -> None:
    """Handles table deletion"""
    password = gp.getpass("You are about to wipe account info. " +
                          "Enter password to confirm: ")
    os.system('clear')
    if not bcrypt.checkpw(password.encode(),
                          database.retrieve_password()):
        print("*Password incorrect. Aborted*")
        time.sleep(1)
    else:
        print("Dropping table...")
        time.sleep(1)
        database.drop_tables()


def check_database_empty(database: db.Database) -> bool:
    """Return True if <database> is empty, that is it has
    no entries. Otherwise, return False.
    """
    if database.is_empty():
        print("Database is empty...")
        time.sleep(1)
        os.system('clear')
        return True
    return False


def fuzzy_search(database: db.Database) -> list:
    """
    Prompt the user for a query and return a list
    containing items that the fuzzy search yields.
    """

    search_input = input("\nEnter search: ").lower().strip(" ")
    results = [item for item in database.query_database()
               if searching.is_found(search_input, item.site)
               or searching.is_found(search_input, item.username)]
    os.system('clear')
    if not results:
        print('No results found')
        time.sleep(1)
        os.system('clear')
    return results


# ======================Search Menu Logic========================

def invoke_menu(input_list: list):
    """
    Display the meny of options and prompt the user
    to select a valid option. Retrieve the password
    with the associated selection.

    """
    options = build_menu_options(input_list)
    if not options:
        print("No items found")
        time.sleep(1)
        os.system('clear')
    show_menu(options)
    print('\n')
    while True:
        user_input = input("Enter option: ").strip()
        if user_input.isnumeric() and int(user_input) <= len(options):
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

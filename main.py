#!/usr/bin/env python3

import os
import pyperclip
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
from searching import levenshtein_distance


class PasswordError(Exception):
    """An exception that should be raised if the
    inputted password is incorrect."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""

        super().__init__(message)


def run():
    """Initialize the program"""

    # Create database handler object
    database_handler = db.DatabaseHandler()
    os.system('clear')

    print("======================Password" +
          "Manager v1.1.1======================")

    # Handle password entry
    trigger = handle_database_input(database_handler)
    key = key_generator(handle_password(trigger, database_handler))
    # Initialize menu options
    user_input = input("\nOptions:\n" + "1. Show entries\n" +
                       "2. Add new entry\n" +
                       "3. Update existing entry\n" +
                       "4. Delete existing entry\n" +
                       "5. Reset database\n" + "6. Exit\n")
    while True:
        os.system('clear')
        if user_input == "1":
            os.system('clear')
            search_input = input("\nOptions:\n" + "1. Search by site\n" +
                                 "2. Search by username\n" + "3. Show all\n")
            os.system('clear')
            if search_input == '1':
                show_selected_site(database_handler, key)
            elif search_input == '2':
                show_selected_username(database_handler, key)
            elif search_input == '3':
                show_all_data(database_handler, key)
            elif search_input == '4':
                show_search_query(database_handler, key)
        elif user_input == "2":
            handle_data_input(database_handler, key)
        elif user_input == "3":
            handle_row_update(database_handler, key)
        elif user_input == "4":
            handle_row_delete(database_handler)
        elif user_input == "5":
            confirm = input("Are your sure? (Y/n)\n")
            if confirm == 'Y':
                handle_table_delete(database_handler)
        elif user_input == "6":
            return 0
        user_input = input("\nOptions:\n" + "1. Show entries\n" +
                           "2. Add new entry\n" +
                           "3. Update existing entry\n" +
                           "4. Delete existing entry\n" +
                           "5. Reset database\n" + "6. Exit\n")


def handle_database_input(database_handler):
    """Return True if the database already exist. If not, create the database
    and return False"""
    if not os.path.exists('./account_database.db'):
        print("Creating account database...")
        database_handler.create_database()
        return False
    print("Accessing database...")
    return True


def handle_password(trigger: bool, database_handler):
    """Return the user-inputted password as a string. If database is
    already created, check the inputted password with database password.
    Otherwise, prompt user to create a password for the database"""
    if trigger:
        p_input = getpass("Enter your password: ")
        if not checkpw(p_input.encode(), database_handler.retrieve_password()):
            raise Exception("Incorrect password")
    else:
        while True:
            p_input = getpass("Enter a password for database: ")
            p_input1 = getpass("Re-enter the password: ")
            if p_input == p_input1:
                database_handler.set_password(hash_password(p_input))
                break
            print("*Passwords do not match*")
    return p_input


def show_search_query(database_handler, key: bytes):
    """Prompt the user to enter a search query and print all
    account information associated with that site. If multiple
    queries are found, have the user select."""

    search_input = input("\nEnter search: ").lower().strip(" ")
    queries = database_handler.query_database()
    if queries == {}:
        print("*Info not found*")
    elif len(queries) > 1:
        all = set()
        for site in queries:
            if levenshtein_distance(search_input, site) < 5:
                for item in queries[site]:
                    all.add(item)
        print(all)
    else:
        pass


def show_selected_site(database_handler, key: bytes):
    """Prompt the user to enter a site and print all account information
    associated with that site"""
    site_input = input("\nEnter site: ").lower().strip(" ")
    queries = database_handler.query_database(site_input, None)
    if queries == {}:
        print("*Info not found*")
    else:
        print("\n============Account Info============")
        for site in queries.keys():
            print("*** " + site + ":")
            for item in queries[site]:
                print(item.username, decrypt_password(item.password, key))
    print("====================================")


def show_selected_username(database_handler, key: bytes):
    """Prompt the user to enter a site and print all account information
    associated with that site"""
    user_input = input("\nEnter username: ").lower().strip(" ")
    queries = database_handler.query_database(None, user_input)
    if queries == {}:
        print("*Info not found*")
    else:
        print("\n============Account Info============")
        for site in queries:
            for item in queries[site]:
                if item.username == user_input:
                    print("*** " + site + ":")
                    print(item.username, decrypt_password(item.password, key))
    print("====================================")


def show_all_data(database_handler, key: bytes):
    """Print all account information in the database"""
    queries = database_handler.query_database()
    print("\n============Account Info============")
    for site in queries:
        print("*** " + site + ":")
        for item in queries[site]:
            print(item.username, decrypt_password(item.password, key))
    print("====================================")


def handle_data_input(database_handler, key: bytes):
    """Prompts the user to enter account information and store it into the
    Account table in database as a row"""
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")
    if database_handler.query_database(site, username) != {}:
        print("*Item already exists*")
    else:
        try:
            length = input("Password length? ")
            password = Passgen(int(length)).gen_password()
            database_handler.insert_data(site, username,
                                         encrypt_password(password, key))
            pyperclip.copy(password)
        except ValueError:
            print("Invalid entry")


def handle_row_update(database_handler, key: bytes):
    """Prompts the user to enter account information to update that row
    with a new generated password"""
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")
    if database_handler.query_database(site, username) == {}:
        print("*Item not found*")
    else:
        length = input("Length? ")
        password = Passgen(int(length)).gen_password()
        new_password = encrypt_password(password, key)
        database_handler.update_item(site, username, new_password)
        pyperclip.copy(password)


def handle_row_delete(database_handler):
    """Handles row deletion"""
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")
    if database_handler.query_database(site, username) == {}:
        print("*Item not found*")
    else:
        print("*Account info deleted*")
        database_handler.delete_row(site, username)


def handle_table_delete(database_handler):
    """Handles table deletion"""
    password = getpass("You are about to wipe account info." +
                       "Enter password to confirm: ")
    if not checkpw(password.encode(), database_handler.retrieve_password()):
        print("*Password incorrect. Aborted*")
    else:
        print("Dropping table...")
        database_handler.drop_tables()

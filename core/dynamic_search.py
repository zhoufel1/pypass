import os
import search
import database as db
from getch import Getch
from constants import ENTER, BACKSPC, ESC


def user_enter_query(database: db.Database) -> str:
    os.system('tput civis')
    user_search = ''

    while True:
        os.system('clear')
        print('Enter search: ' + user_search)
        results = fuzzy_search(user_search, database)
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        project_menu(build_menu_options(results))

        user_input = Getch()()
        if user_input == ENTER and results != []:
            break
        elif user_input == ENTER and results == []:
            continue
        elif user_input == BACKSPC and user_search == '':
            pass
        elif user_input == BACKSPC and user_search != '':
            user_search = user_search[:-1]
        elif user_input == ESC:
            return ESC
        elif user_input.isprintable():
            user_search += user_input.lower()

    return user_search


def project_menu(menu_options: dict) -> None:
    if not menu_options:
        print("Nothing found")
    else:
        for item in menu_options:
            print('[' + str(item) + ']' +
                  ' Site: ' +
                  menu_options[item].site +
                  '\n    User: ' +
                  menu_options[item].username)


def build_menu_options(input_list: list) -> list:
    results = {}
    for i in range(len(input_list)):
        results[i + 1] = input_list[i]
    return results


def check_database_empty(database: db.Database) -> bool:
    if database.is_empty():
        print('Database is empty...')
        input('\nPress Enter to continue...')
        return True
    return False


def fuzzy_search(search_input: str, database: db.Database) -> list:
    if not search_input:
        results = database.query_database()
    else:
        results = [item for item in database.query_database()
                   if search.is_found(search_input, item.site)
                   or search.is_found(search_input, item.username)]
    return results

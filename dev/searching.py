import search_algo
from database import AccountDatabase
from system import clear_screen, hide_cursor, show_cursor, getch
from constants import ENTER, BACKSPC, ESC, UP, DOWN, LEFT


def show_searcher(database: AccountDatabase, key: bytes) -> str:
    user_search = ''

    data = [f'line {i}' for i in range(80)]
    max_lines = 30
    lower, upper = 0, max_lines

    while True:
        clear_screen()
        print("> " + user_search + "█")
        print("10/20\n") # TEMP

        for i in range(lower, upper):
            print(data[i])

        input_char = getch()
        if input_char == DOWN and upper < len(data):
            lower += 1
            upper += 1
        elif input_char == UP and lower > 0:
            lower -= 1
            upper -= 1
        elif input_char == ESC:
            return 0
        # elif input_char == BACKSPC:
            # user_search = user_search[:-1]
        # elif input_char.isprintable():
            # user_search += input_char.lower()

hide_cursor()
show_searcher(None, None)
show_cursor()

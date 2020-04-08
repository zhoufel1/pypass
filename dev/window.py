#!/usr/bin/env python3
from __future__ import annotations
from typing import Callable, Any
from system import *
from constants import *

import shutil
import os
from typing import *
import sys
import tty
import termios

class Window:
    def __init__(self) -> None:
        self.operations = []

    def add_operation(self, function: Callable, *args: Any) -> None:
        self.operations.append((function, [arg for arg in args]))

    def run_window(self) -> list:
        clear_screen()
        inputs = []
        for pair in self.operations:
            operation = pair[0]
            args = pair[1]
            if len(args) == 1:
                if operation == input:
                    inputs.append(operation(args[0]))
                else:
                    operation(args[0])
        return inputs


def main():
    data = [f"{n} line" for n in range(1, 100)]
    scroll_test(data)

    # for _ in range(10):
        # print("TEST")
    # while (True):
        # t_size = shutil.get_terminal_size()
        # print(f"r: {t_size[0]}, c: {t_size[1]}")

def scroll_test(data: List[str]):
    max_lines = shutil.get_terminal_size()[1]
    # max_lines = 15
    if max_lines < len(data):
        lower, upper = 0, max_lines
        data.insert(0, 0)
    else:
        lower, upper = 0, len(data)
    while True:
        clear_screen()
        for i in range(lower, upper):
            print(data[i])
        key = getch()
        if key == "\x1b":
            return 0
        elif key == "j" or key == DOWN and upper < len(data):
            lower += 1
            upper += 1
        elif key == "k" and lower > 0:
            lower -= 1
            upper -= 1

def getch():
    file_desc = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_desc)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)
    return char

def print_lines():
    print(shutil.get_terminal_size()[1])


def clear_screen():
    os.system("clear")

if __name__ == '__main__':
    main()

"""
* Refresh on terminal dimension change (maybe parallel process which detects when a window resize occurs)
* Implement scrolling
* Implement dynamic window


"""

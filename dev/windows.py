#!/usr/bin/env python3
from __future__ import annotations
import shutil
import os
from typing import *
import sys
import tty
import termios



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
        elif key == "j" and upper < len(data):
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

import os
import sys
import tty
import termios


def clear_screen():
    os.system("clear")


def hide_cursor():
    os.system("tput civis")


def show_cursor():
    os.system("tput cnorm")


def getch():
    file_desc = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_desc)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)
    return char

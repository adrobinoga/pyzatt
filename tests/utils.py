#!/usr/bin/python3.5

"""
Functions to print in a specific format the steps of a given test.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

from colorama import Fore, Style

hhh = 80*'#'

def print_info(s):
    """
    Prints text in green bright font.

    :param s: String, text to be printed.
    :return: None.
    """
    print(Style.BRIGHT + Fore.GREEN + s +Style.RESET_ALL)

def print_header(s):
    """
    Prints a title in green bright font.
    :param s: String, text to be printed.
    :return: None.
    """
    print_info('\n' + hhh + '\n#\t' + s + '\n')
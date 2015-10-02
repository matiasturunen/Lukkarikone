# ------------------------------------------------------------------------------
# Name:        debug.py
# Purpose:     Helper functions for testing and debugging
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------


def printList(listToPrint, emptyline=True):
    """Print given list to console.

        Keyword arguments:
        listToPrint -- List to be printed
        emptyline -- Will there be empty line after each item in list
    """
    for item in listToPrint:
        try:
            print(item)
            if emptyline:
                print("")
        except UnicodeError as e:
            print("Skipping print due error", e)
        


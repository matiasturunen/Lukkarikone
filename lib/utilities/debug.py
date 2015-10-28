# ------------------------------------------------------------------------------
# Name:        debug.py
# Purpose:     Helper functions for testing and debugging
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------


def printList(listToPrint, emptyline=True, depth=0):
    """Print given list to console.

        Keyword arguments:
        listToPrint -- List to be printed
        emptyline -- Will there be empty line after each item in list
        depth -- internal argument to make printing nested lists more readable
    """
    for item in listToPrint:
        try:
            if isinstance(item, list):
                printList(item, emptyline, depth + 1)
            else:
                print('    '*depth + str(item))
                if emptyline:
                    print("")
        except UnicodeError as e:
            print("Skipping print due error", e)
        


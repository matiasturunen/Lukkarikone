# ------------------------------------------------------------------------------
# Name:        Main.py
# Purpose:	   Handle all the things!!
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------
from lib.utilities import links, html, scheludes
from lib.utilities import debug
from lib.models import Link
import re
import os


uniURL = "https://uni.lut.fi"
scheludeListURL = uniURL + "/fi/lukujarjestykset1"

def printMenu():
    print("""
    1) Load scheludes to memory
    2) Save scheludes to disk
    3) search course
    0) Exit
    """)


def menu():
    sche = None
    while True:
        printMenu()
        option = input("What to do: ")
        if (option == "0"):
            break
        elif (option == "1"):
            print("Loading...")
            sche = scheludes.getLocalScheludesJSON()
            print("Loading complete!")
        elif (option == "2"):
            print("Saving...")
            scheludes.saveScheludes(sche)
            print("Saving complete!")
        elif (option == "3"):
            print ("Rule can be course name or code")
            rule = input("Give search rule: ")
            print("Searching...")
            matched = scheludes.findAllCourses(rule, sche)
            print("")
            debug.printList(matched)



def main():
    # local = True    # set False to load scheludes from internet
    # if ( local ):
    #     sche = scheludes.getLocalScheludesHTML()
    #     scheludes.saveScheludes(sche)
    # else:
    #     sche = scheludes.getScheludes(uniURL, scheludeListURL)
    menu()

if __name__ == '__main__':
    main()

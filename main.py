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
    1) Load local scheludes to memory (HTML, very slow)
    2) Load web scheludes to memory (HTML, very slow)
    3) Load local scheludes to memory (JSON, almost instant)
    4) Save scheludes to disk
    5) search course
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
            sche = scheludes.getLocalScheludesHTML()
            print("Loading complete!")

        elif (option == "2"):
            print("Loading...")
            sche = scheludes.getScheludes(uniURL, scheludeListURL)
            print("Loading complete!")

        elif (option == "3"):
            print("Loading...")
            sche = scheludes.getLocalScheludesJSON()
            print("Loading complete!")

        elif (option == "4"):
            print("Saving...")
            scheludes.saveScheludes(sche)
            print("Saving complete!")

        elif (option == "5"):
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

# ------------------------------------------------------------------------------
# Name:        scheludes.py
# Purpose:     Collection of scheludes related methods
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------
import os
import re
from lib.utilities import links, html
from lib.utilities import debug

def getLocalScheludeNames():
    """Get all locally stored schelude names
    """
    folder = "scheludes"
    prefix = "scheludePage_"

    prefLen = len(prefix)

    try:
        # get all filenames in the folder
        fileNames = os.listdir(folder)
    except Exception as e:
        print(e)
        raise e

    scheludeNames = []
    for f in fileNames:
        if (prefix == f[:prefLen]):
            # file prefix matched
            scheludeNames.append(f[prefLen:])

    return scheludeNames


def getLocalScheludePage(scheludeName):
    """Get locally saved html version of schelude
    """
    folder = "scheludes/"
    prefix = "scheludePage_"

    schelude = ""
    print ("Loading local file")
    try:
        f = open(folder + prefix + scheludeName, "r")
        schelude = f.read()
        f.close()
    except Exception as e:
        print (e)

    return schelude


def getLocalScheludes():
    """Get all locally stored scheludes
    """
    scheludeList = []

    names = getLocalScheludeNames()
    for name in names:
        page = getLocalScheludePage( name )
        print("\n" + name + "\n")
        scheludeList.append( objectifySchelude( page ) )


def getScheludes(uniURL, scheludeListURL):
    """Get scheludes from internet

        Keyword arguments:
        uniURL -- url to UNI web portal
        scheludeListURL -- url to page which contains links to scheludes
    """

    # get links to schelude pages
    linklist = links.getScheludeLinks(scheludeListURL)
    scheludeList = []
    for item in linklist:
        scheludePage = html.getHTML(uniURL + item.url)
        if( not scheludePage ):
            print("Skipping invalid page")
            continue
        print(item.name)

        # save to file to save internet usage
        try:
            f = open("scheludes/scheludePage_" + item.name, "w")
            f.write(scheludePage)
            f.close()
        except Exception as e:
            pass

        scheludeList.append( objectifySchelude( scheludePage ) )

    return scheludeList

def saveScheludes(scheludes):
    """Save all scheludes in custom format
    """
    pass


def saveSchelude(schelude):    
    """Save single schelude in custom format
    """
    pass


def objectifySchelude(scheludePage):
    """Convert html type scheludepage to objects for easier use
    """

    # match all groups of underscore that are longer thar 10 chars
    splitPattern = r'_{10,}'
    splitProg = re.compile(splitPattern)

    # extract individual courses from scheludepages
    courses = html.listifyHTML(scheludePage, splitProg, "body")
    debug.printList(courses)

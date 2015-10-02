# ------------------------------------------------------------------------------
# Name:        Main.py
# Purpose:	   Handle all the things!!
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------
from lib.utilities import links, html
from lib.utilities import debug
from lib.models import Link
import re


uniURL = "https://uni.lut.fi"
scheludeListURL = uniURL + "/fi/lukujarjestykset1"

def getScheludes(local=False):
    """Get all scheludes and return them as objects

        Keyword arguments:
        local -- Determine if scheludes should be loaded from local filesystem
            instead of internet 
    """
    # get links to schelude pages
    linklist = links.getScheludeLinks(scheludeListURL)

    scheludes = []
    #splitPattern = r'(<\/?table[^>]+(class=(\'|\")footer-border-args(\'|\"))+>)'
    #splitProg = re.compile(splitPattern)

    splitPattern = r'_{10,}'
    splitProg = re.compile(splitPattern)
    for item in linklist:
        if ( local ):
            scheludePage = loadLocalSchelude(item.name)
        else:
            scheludePage = html.getHTML(uniURL + item.url)
        if( not scheludePage ):
            print("Skipping invalid page")
            continue
        print(item.name)

        if ( not local ):
            # save to file if not from local storage
            try:
                f = open("scheludes/scheludePage_" + item.name, "w")
                f.write(scheludePage)
                f.close()
            except Exception as e:
                pass

        # extract individual courses from scheludes
        courses = html.listifyHTML(scheludePage, splitProg, "body")
        debug.printList(courses)
        #break
            
def loadLocalSchelude(pagename):
    folder = "scheludes/"
    prefix = "scheludePage_"

    schelude = ""
    print ("Loading local file")
    try:
        f = open(folder + prefix + pagename, "r")
        schelude = f.read()
        f.close()
    except Exception as e:
        print (e)

    return schelude

def main():
    local = True    # set False to load scheludes from internet
    scheludes = getScheludes(local)


if __name__ == '__main__':
    main()

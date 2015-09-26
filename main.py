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


uniURL = "https://uni.lut.fi"
scheludeListURL = uniURL + "/fi/lukujarjestykset1"

def main():
    # get links to schelude pages
    linklist = links.getScheludeLinks(scheludeListURL)
    debug.printList(linklist)

    for item in linklist:
        scheludePage = html.getHTML(uniURL + item.url)
        if( not scheludePage):
            print("Skipping invalid page")
            continue
        print(item.name)
        print(scheludePage)
        print("")


if __name__ == '__main__':
    main()

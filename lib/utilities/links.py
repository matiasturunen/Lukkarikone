# ------------------------------------------------------------------------------
# Name:        links.py
# Purpose:     Utility functions for handling and finding links
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------
import re
from lib.static.htmldom import htmldom
from lib.models import Link
from lib.utilities import html


def getScheludeLinks(scheludeListUrl):

    # rough CSS path to links, eases future processing
    linksCssPath = [
        "div",
        "section",
        "p",
        "a"
    ]
    
    page = html.getHTML(scheludeListUrl)
    if(page == ""):
        print("Empty page")

    # create htmldom element with html we just got
    dom = htmldom.HtmlDom().createDom(page)
    
    # delete page to save some memory
    del(page)

    findString = " ".join( linksCssPath )

    # get all link items
    linkitems = dom.find( findString ).html()
    linkitems = linkitems.split("</a>")

    # filter out only valid links
    validLinks = filter(isValidLink, linkitems)

    result = []

    # add links to result list as Link objects
    for link in validLinks:
        result.append( Link( getLinkName(link), getLinkUrl(link) ) )

    return result

def isValidLink(linkString):
    # check if given string contains valid link 
    linkPattern = r'(")(\/c\/document_library\/get_file\?.*)" '
    return re.search(linkPattern, linkString)

def getLinkUrl(linkString):
    # return link url from linkstring, if its valid. False otherwise
    linkPattern = r'(")(\/c\/document_library\/get_file\?.*)" '
    match = re.search(linkPattern, linkString)
    if (match):
        return match.group(2)
    return False

def getLinkName(linkString):
    # return link name from linkstring, if its valid. False otherwise
    pattern = r'("\/c\/document_library\/get_file\?.*">)\s*(.*)'
    match = re.search(pattern, linkString)
    if (match):
        return match.group(2)
    return False

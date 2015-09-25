# ------------------------------------------------------------------------------
# Name:        linkutility.py
# Purpose:     
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------
import urllib.request as request
from static.htmldom import htmldom
import re


def getScheludeLinks():


    linksCssPath = [
        "div",
        "section",
        "p",
        "a"
    ]
    # TODO: make it use configfiles instead of static urls
    response = request.urlopen("https://uni.lut.fi/fi/lukujarjestykset1")
    html = response.read()
    # convert html to string (originally bytes)
    html = html.decode(encoding='UTF-8')

    # create htmldom element with html we just got
    dom = htmldom.HtmlDom().createDom(html)
    
    findString = " ".join( linksCssPath )

    # get all link items
    linkitems = dom.find( findString ).html()
    linkitems = linkitems.split("</a>")

    # filter out only valid links
    validLinks = filter(isValidLink, linkitems)

    for link in validLinks:
        print("URL:", getLinkUrl(link))
        print("Name:", getLinkName(link))
        print("")

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

getScheludeLinks()

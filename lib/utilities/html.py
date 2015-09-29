# ------------------------------------------------------------------------------
# Name:        html.py
# Purpose:	   web page related stuff
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------
import urllib.request as request
import re
from lib.static.htmldom import htmldom


def getHTML(url, encodeWith="UTF-8"):
    """Get HTML page from url

        As default, html is encoded with UTF-8.

        Keyword arguments:
        url -- url which leads to html page
        encodeWith -- encoding for resulted html. Defaults to UTF-8. Can be
            changed to other encodings as well (not tested), or left to be empty
            string if no encoding is needed (will return bytes instead)

        will return False if page is not in html
    """
    response = request.urlopen(url)
    html = response.read()

    if( not checkIfHTML(html, encodeWith) ):
        print("Page is NOT in html!!")
        return False
    
    if ( encodeWith != "" ):
        # convert html to string (originally bytes)
        try:
            html = html.decode(encoding=encodeWith)
        except UnicodeError:
            # just catch error and show message in console
            print("UnicodeError happened.")

    return html


def checkIfHTML(data, encodeWith="UTF-8"):
    """Check if given data is actually html and not something like PDF
    """

    # remove all leading spaces
    data = data.lstrip()

    try:
        firstchars = data[0:9].decode(encoding=encodeWith)
        print ("chars: " + firstchars)

        # check that data starts with doctype definition
        if (firstchars != "<!DOCTYPE"):
            return False
    except UnicodeError:
        return False

    return True


def listifyHTML(pageHTML, splitRule, path=None):
    """Create list from html using given rule

        Keyword arguments:
        pageHTML -- raw HTML. Must begin with DOCTYPE definition
        splitRule -- Set of characters to define where to split.
            This uses python's split() function
        path -- CSS path which narrows down section we are going
            to be splitting into list
            must be in string format
    """
    # create htmldom element from the page
    dom = htmldom.HtmlDom().createDom(pageHTML)

    itemList = pageHTML
    print(path)
    if ( path != None ):
        # narrowed down version of html page
        itemList = dom.find( path ).html()

    itemList = itemList.split( splitRule )

    return itemList

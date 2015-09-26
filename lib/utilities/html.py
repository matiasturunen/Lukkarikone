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


def getHTML(url, encodeWith="UTF-8"):
    """Get HTML page from url

        As default, html is encoded with UTF-8.

        Keyword arguments:
        url -- url which leads to html page
        encodeWith -- encoding for resulted html. Defaults to UTF-8. Can be
            changed to other encodings as well (not tested), or left to be empty
            string if no encoding is needed (will return bytes instead)

        will return empty string if page is not in html
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
            print("UnicodeError happened.")

    return html


def checkIfHTML(data, encodeWith="UTF-8"):
    """Check if given data is actually html and not something like PDF
    """
    try:
        # '<!DOCTYPE' can fit in 9 chars, 
        # but it seems that there can be some leading spaces
        firstchars = data[0:13].decode(encoding=encodeWith)
        print ("chars",firstchars)

        # check that data starts with doctype definition
        pattern = r'\s*<!DOCTYPE.*'
        if ( not re.search(pattern, firstchars)):
            return False
    except UnicodeError:
        return False

    return True

        
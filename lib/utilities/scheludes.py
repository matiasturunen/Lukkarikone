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
from lib.models import Course, Lesson, Schelude
from bs4 import BeautifulSoup
import json


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
    #print ("Loading local file")
    try:
        f = open(folder + prefix + scheludeName, "r")
        schelude = f.read()
        f.close()
    except Exception as e:
        print (e)

    return schelude


def getLocalScheludesHTML():
    """Get all locally stored scheludes that are in HTML format
    """
    scheludeList = []

    names = getLocalScheludeNames()
    for name in names:
        page = getLocalScheludePage( name )
        #print("\n" + name + "\n")
        s = objectifySchelude( page, name )
        #print(json.dumps(s.toDict(), indent=2))
        scheludeList.append( s )
    
    return scheludeList

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

        scheludeList.append( objectifySchelude( scheludePage, item.name ) )

    return scheludeList

def saveScheludes(scheludes):
    """Save all scheludes in custom format

        Keyword arguments:
        scheludes -- list of Schelude objects
    """
    
    for schelude in scheludes:
        schelude.saveToFile()


def saveSchelude(schelude):    
    """Save single schelude in custom format
    """
    pass


def objectifySchelude(scheludePage, scheludeName):
    """Convert html type scheludepage to objects for easier use

        returns list containing all courses as objects
    """

    # match all groups of underscore that are longer thar 10 chars
    splitPattern = r'_{10,}'
    splitProg = re.compile(splitPattern)

    # extract individual courses from scheludepages
    courses = html.listifyHTML(scheludePage, splitProg, "body")
    
    courseList = []
    for course in courses:

        soup = BeautifulSoup(course)
        spreadsheet = soup.find_all("table", "spreadsheet")

        result = []

        if (len(spreadsheet) == 0):
            continue

        # there is actualy only one item in the spreadsheet
        table = spreadsheet[0]

        table = str(table)                    # convert to string
        table = table.strip()                 # try stripping whitespace
        table = table.replace("\n", "")       # remove all linebreaks
        table = table.replace("</td>", ";")   # replace </td> with ;
        table = table.replace("</tr>", "|\n") # replace </tr> with | and newline
        table = html.stripTags(table)         # strip all remaining html tags
        table = re.sub(r' {2,}', " ", table)  # replace all whitespace sequences 
        
        tableRows = table.split("|")

        rowNumber = 0
        courseCode = None
        courseName = None
        lessons = []
        for tableRow in tableRows:  # each row is one lesson
            tableCells = tableRow.split(";")

            """ tableCells structure
                index   content
                  0       Course code and name
                  1       Period number
                  2       Week
                  3       Day of Week
                  4       Starting time
                  5       Ending time
                  6       Classroom number or name
                  7       Description
            """
            if(rowNumber == 0):
                # we are not interested at the first row
                rowNumber += 1
                continue
            
            if (len(tableCells) < 8):
                # we need all eight table columns
                continue


            if (courseCode == None):
                courseCode = tableCells[0].split(" - ")[0]
            if (courseName == None):
                if(" - " in tableCells[0]):
                    courseName = tableCells[0].split(" - ")[1]

            # create new lesson
            lesson = Lesson()
            lesson.lessonType = ""
            lesson.period = tableCells[1]
            lesson.week = tableCells[2]
            lesson.dayOfWeek = tableCells[3]
            lesson.startTime = tableCells[4]
            lesson.endTime = tableCells[5]
            lesson.room = tableCells[6]
            lesson.description = tableCells[7]

            lessons.append(lesson)

        courseObj = Course(courseCode, courseName)
        courseObj.lessons = lessons

        courseList.append(courseObj)

    schelude = Schelude(scheludeName)
    schelude.courses = courseList

    return schelude
        
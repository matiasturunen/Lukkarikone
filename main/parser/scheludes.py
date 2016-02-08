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
from . import links, html
from ..models import Course, Lesson, Schelude, Period, LessonType
from bs4 import BeautifulSoup
import json
import datetime


def getLocalScheludeNames(folder, prefix=""):
    """Get all locally stored schelude names

        Keyword arguments:
        folder -- Folder that contains the files
        prefix -- Filename prefix
    """

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


def getLocalScheludeFile(scheludeName, folder, prefix=""):
    """Get locally saved schelude file contents

        Keyword arguments:
        folder -- Folder that contains the files
        prefix -- Filename prefix
    """

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

    folder = "scheludes/"
    prefix = "scheludePage_"

    scheludeList = []

    names = getLocalScheludeNames(folder, prefix)
    for name in names:
        page = getLocalScheludeFile( name, folder, prefix )
        s = parseScheludeHTML( page, name )
        scheludeList.append(s)
    
    return scheludeList


def getLocalScheludesJSON():
    """Get all locally stored scheludes that are in JSON format
    """

    folder = "scheludes/objects/"

    scheludeList = []

    names = getLocalScheludeNames(folder)
    for name in names:
        jsonfile = getLocalScheludeFile(name, folder)
        s = parseScheludeJSON( jsonfile )
        scheludeList.append(s)

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
        #print(item.name)

        # save to file to save internet usage
        # not in django version
        """
        try:
            f = open("scheludes/scheludePage_" + item.name, "w")
            f.write(scheludePage)
            f.close()
        except Exception as e:
            pass
        """

        scheludeList.append( parseScheludeHTML( scheludePage, item.name ) )
        

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
    schelude.saveToFile()


def parseScheludeHTML(scheludePage, scheludeName):
    """Convert html type scheludepage to objects for easier use
        This is basically a parser

        returns list containing all courses as objects
    """

    # extract individual courses from scheludepages
    soup = BeautifulSoup(scheludePage)
    courses = soup.find_all("table", "spreadsheet")
    
    # create new schelude
    schelude = Schelude()
    schelude.name = scheludeName
    schelude.save()
    
    courseList = []
    lessonAmount = 0
    courseAmount = 0
    for course in courses:

        result = []

        if (len(course) == 0):
            continue
        
        courseObj = Course()
        courseObj.name = ""     # default value
        courseObj.code = ""     # default value
        courseObj.schelude = schelude
        courseObj.save()
        courseAmount += 1

        # start parsing table
        course = str(course)                    # convert to string
        course = course.strip()                 # try stripping whitespace
        course = course.replace("\n", "")       # remove all linebreaks
        course = course.replace("</td>", ";")   # replace </td> with ;
        course = course.replace("</tr>", "|")   # replace </tr> with |
        course = html.stripTags(course)         # strip all remaining html tags
        course = re.sub(r' {2,}', " ", course)  # replace all whitespace sequences 
        
        tableRows = course.split("|")

        rowNumber = 0
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
                # we need at least eight table columns
                continue
            
            lessonData = getLessonData(tableCells[0])

            # get course name and code only once
            courseObjChanged = False
            if (courseObj.code == ""):
                courseObj.code = lessonData["code"]
                courseObjChanged = True
            if (courseObj.name == ""):
                courseObj.name = lessonData["name"]
                courseObjChanged = True
                
            if (courseObjChanged):
                courseObj.save()

            # create new lesson
            lesson = Lesson()
            
            # Lesson base information
            lesson.lessonType = lessonData["type"]
            lesson.name = lessonData["name"]
            lesson.course = courseObj
            
            if (len(tableCells) == 8):
                # schelude has eight columns
                lesson.week = tableCells[2]
                lesson.dayOfWeek = tableCells[3]
                lesson.startTime = getParsedTime(tableCells[4])
                lesson.endTime = getParsedTime(tableCells[5])
                lesson.room = tableCells[6]
                lesson.description = tableCells[7]
                
            elif (len(tableCells) >= 9):
                # schelude has nine columns
                lesson.week = tableCells[3]
                lesson.dayOfWeek = tableCells[4]
                lesson.startTime = getParsedTime(tableCells[5])
                lesson.endTime = getParsedTime(tableCells[6])
                lesson.room = tableCells[7]
                lesson.description = tableCells[8]
                
            else:
                # How did you get here?
                print ("How did you get here??")
                print ("Empty course incoming!")
                continue
            
            
            # save lesson so we can add manyToNany relation to it
            lesson.save()
            lesson.period = getPeriod(tableCells[1])
            lesson.save()
            
            lessonAmount += 1
    
    print ("Added {0} lessons to {1} courses in schelude {2}.".format(lessonAmount, courseAmount, scheludeName))
    return True


def parseScheludeJSON(jsonString):
    """Convert schelude json back to objects

        Keyword arguments:
        jsonString -- json formatted string containing schelude values
    """

    jsonObj = json.loads(jsonString)

    courseList = []
    for courseId in jsonObj["courses"]:
        course = jsonObj["courses"][courseId]

        lessonList = []
        for lessonId in course["lessons"]:
            lesson = course["lessons"][lessonId]

            # create lesson
            lessonObj = Lesson()
            lessonObj.lessonType = ""
            lessonObj.period = lesson["period"]
            lessonObj.week = lesson["week"]
            lessonObj.dayOfWeek = lesson["dayOfWeek"]
            lessonObj.startTime = lesson["startTime"]
            lessonObj.endTime = lesson["endTime"]
            lessonObj.room = lesson["room"]
            lessonObj.description = lesson["description"]
            #lessonObj.name = lesson["name"]

            lessonList.append(lessonObj)

        # create course
        courseObj = Course()
        courseObj.name = course["name"]
        courseObj.code = course["code"]
        courseObj.lessons = lessonList
        
        courseList.append(courseObj)

    # create schelude
    schelude = Schelude()
    schelude.name = jsonObj["name"]
    schelude.courses = courseList

    return schelude


def getLessonData(lessonNameCode):
    """Extracts lesson type, name and code from string
    """
    if (" - " in lessonNameCode):
        splits = lessonNameCode.split(" - ")
        code = splits[0]
        name = splits[1]
    else:
        code = ""
        name = lessonNameCode

    if ("/" in name):
        splits2 = name.split("/")
        name = splits2[0]
        lessonType = splits2[1]
        lessonType = lessonType.strip()
    else:
        lessonType = ""
        
    # get lessontype code right
    # codes - These are hardcoded fixtures
    # 1 - Lecture / Luento
    # 2 - Exercise / Harjoitus
    # 3 - Combination of 1 and 2
    # 4 - Other / Muu - DEFAULT
    # 5 - Seminaari
    # 6 - Demoluento
    # 7 - intensive
    typeCodes = {
        "L": 1,
        "H": 2,
        "HR": 2,
        "L/H": 3,
        "H/L": 3,
        "L+H": 3,
        "H+L": 3,
        "S": 5,
        "DL": 6,
        "INT": 7
        
    }
    
    typeCode = 4    # default
    if (lessonType != ""):
        # try getting lessontype to be something else than other...
        try:
            typeCode = typeCodes[lessonType]
        except KeyError:
            # type not found, use default
            print ("Lessontype {0} not found.".format(lessonType))
            pass
        except Exception as e:
            # Other error happened
            print ("Error: " + e)
        
    else:
        # does this even need an else block?
        pass
    
    # try/except would be nice for this, but if we can't find LessonType saving lesson is impossible
    type = LessonType.objects.get(pk=typeCode)

    return {
        "type": type,
        "name": name,
        "code": code
    }


def getParsedTime(hours=0, minutes=0):
    try:
        hours = int(hours)
        minutes = int(minutes)
        
        return datetime.time(hours, minutes)
        
    except ValueError:
        return datetime.time(0,0)
        


def findCourses(searchRule, schelude):
    """Search for course in specific schelude

        Keyword arguments:
        searchRule -- Rule which is used for searching
        schelude -- schelude object
    """  

    matched = []
    for course in schelude.courses:
        if (course.name != None and searchRule in course.name):
            matched.append(course)
        elif (course.code != None and searchRule in course.code):
            matched.append(course)

    return matched


def findAllCourses(searchRule, scheludes):
    """Search for courses in all scheludes

        Keyword arguments:
        searchRule -- Rule which is used for searching
        scheludes -- schelude object list
    """

    matched = []
    for schelude in scheludes:
        courses = findCourses(searchRule, schelude)
        matched.extend(courses)

    return matched

def getPeriod(periodString): 
    # get period number right
    periodType = "None" # default
    periodNumber = 1    # default
    
    matchPeriod = re.search(r'^\s*periodi\s*([0-4])\s*$', periodString.lower())
    if (matchPeriod):
        periodType = "Normal"
        periodNumber = matchPeriod.group(1)
    else:
        # it was no "normal" period, looking for intensive
        matchIntensive = re.search(r'^\s*int.vko\s*([0-9]+)\s*$', periodString.lower())
        if (matchIntensive):
            periodType = "Intensive"
            periodNumber = matchIntensive.group(1)
        else:
            # not normal nor intensive, going to defaults
            # defaults defined above...
            pass
    
    try:
        period = Period.objects.filter(number=periodNumber, type=periodType)
    except Period.DoesNotExist:
        # create new instance of it
        period = Period()
        period.number = periodNumber
        period.type = periodType
        period.save()
    
    return period
    
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
        # debug break
        return scheludeList

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

    # match all groups of underscore that are longer thar 10 chars
    splitPattern = r'_{10,}'
    splitProg = re.compile(splitPattern)

    # extract individual courses from scheludepages
    courses = html.listifyHTML(scheludePage, splitProg, "body")
    
    # create new schelude
    schelude = Schelude()
    schelude.name = scheludeName
    schelude.save()
    
    courseList = []
    lessonAmount = 0
    courseAmount = 0
    for course in courses:

        soup = BeautifulSoup(course)
        spreadsheet = soup.find_all("table", "spreadsheet")

        result = []

        if (len(spreadsheet) == 0):
            continue
        
        courseObj = Course()
        courseObj.name = ""     # default value
        courseObj.code = ""     # default value
        courseObj.schelude = schelude
        courseObj.save()
        courseAmount += 1

        # there is actualy only one item in the spreadsheet
        table = spreadsheet[0]

        table = str(table)                    # convert to string
        table = table.strip()                 # try stripping whitespace
        table = table.replace("\n", "")       # remove all linebreaks
        table = table.replace("</td>", ";")   # replace </td> with ;
        table = table.replace("</tr>", "|")   # replace </tr> with |
        table = html.stripTags(table)         # strip all remaining html tags
        table = re.sub(r' {2,}', " ", table)  # replace all whitespace sequences 
        
        tableRows = table.split("|")

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
                # we need all eight table columns
                continue

            # get course name and code only once
            courseObjChanged = False
            if (courseObj.code == ""):
                courseObj.code = getCourseNameAndCode(tableCells[0])["code"]
                courseObjChanged = True
            if (courseObj.name == ""):
                courseObj.name = getCourseNameAndCode(tableCells[0])["name"]
                courseObjChanged = True
                
            if (courseObjChanged):
                courseObj.save()

            nameAndType = getLessonTypeAndName(tableCells[0])
            
            # get lessontype code right
            # codes
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
            if (nameAndType["type"] != ""):
                # try getting lessontype to be something else than other...
                try:
                    typeCode = typeCodes[nameAndType["type"]]
                except KeyError:
                    # type not found, use default
                    print ("Lessontype {0} not found.".format(nameAndType["type"]))
                    pass
                except Exception as e:
                    # Other error happened
                    print ("Error: " + e)
                
            else:
                # does this even need an else block?
                pass
            
            #try:
            type = LessonType.objects.get(pk=typeCode)
            #except LessonType.DoesNotExist:
            #    raise Exception("Lessontype not found!!")
            #except:
            #    raise Exception("Unknown error!!!")
            
            # get period number right
            periodType = "None" # default
            periodNumber = 1    # default
            
            matchPeriod = re.search(r'^\s*periodi\s*([0-4])\s*$', tableCells[1].lower())
            if (matchPeriod):
                periodType = "Normal"
                periodNumber = matchPeriod.group(1)
            else:
                # it was no "normal" period, looking for intensive
                matchIntensive = re.search(r'^\s*int.vko\s*([0-9]+)\s*$', tableCells[1].lower())
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
            

            # create new lesson
            lesson = Lesson()
            
            lesson.lessonType = type
            lesson.name = nameAndType["name"]
            lesson.week = tableCells[2]
            lesson.dayOfWeek = tableCells[3]
            lesson.startTime = getParsedTime(tableCells[4])
            lesson.endTime = getParsedTime(tableCells[5])
            lesson.room = tableCells[6]
            lesson.description = tableCells[7]
            lesson.course = courseObj
            
            # save lesson so we can add manyToNany relation to it
            lesson.save()
            lesson.period = period
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


def getLessonTypeAndName(lessonNameCode):
    """Extracts lesson type and name from string
    """
    if (" - " in lessonNameCode):
        splits = lessonNameCode.split(" - ")
        name = splits[1]
    else:
        name = lessonNameCode

    if ("/" in name):
        splits2 = name.split("/")
        name = splits2[0]
        lessonType = splits2[1]
        lessonType = lessonType.strip()
    else:
        lessonType = ""

    return {
        "type": lessonType,
        "name": name
    }


def getCourseNameAndCode(lessonNameCode):
    """Extracts course name and code from string
    """
    if (" - " in lessonNameCode):
        splits = lessonNameCode.split(" - ")
        code = splits[0]
        name = splits[1]
    else:
        code = ""
        name = lessonNameCode

    if ("/" in name):   # name contains lesson type, what we want to remove
        name = name.split("/")[0]

    return {
        "name": name,
        "code": code
    }
    

def getParsedTime(hours=0, minutes=0):
    try:
        hours = int(hours)
        minutes = int(minutes)
    except ValueError:
        return datetime.time(0,0)
        
    t = datetime.time(hours, minutes)
    return t


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


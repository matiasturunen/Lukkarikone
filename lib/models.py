# ------------------------------------------------------------------------------
# Name:        models.py
# Purpose:     Contains all models in this app
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------
from lib import enums
import json

class Link:

    name = ""
    url = ""

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return (self.name + "\n " + self.url)

class Schelude:

    name = ""
    courses = []

    def __init__(self, name=""):
        self.name = name

    def saveToFile(self):
        file = open("scheludes/objects/" + self.name + ".json", "w", encoding="UTF-8")
        file.write(json.dumps(self.toDict(), indent=2))
        file.close()

    def toDict(self):
        arr = {
            "name": self.name,
        }
        cours = {}
        i = 0
        for course in self.courses:
            cours[i] = course.toDict()
            i += 1

        arr["courses"] = cours
        return arr

class Course:

    code = ""
    name = ""
    lessons = [] # list of Lesson objects

    def __init__(self, code, name=""):
        self.code = code
        self.name = name

    def toDict(self):
        arr = {
            "code": self.code,
            "name": self.name,
        }
        les = {}
        i = 0
        for lesson in self.lessons:
            les[i] = lesson.toDict()
            i += 1

        arr["lessons"] = les

        return arr

class Lesson:

    lessonType = ""     # lesson type
    period = 0          # period number
    week = 0            # week number
    dayOfWeek = None    # Day enum
    startTime = 0       # starting hour
    endTime = 0         # ending houd
    room = None         # room name or number
    description = None  # description

    def __init__(self):
        self.week = 0

    def toDict(self):
        arr = {
            "lessonType": self.lessonType,
            "period": self.period,
            "week": self.week,
            "dayOfWeek": self.dayOfWeek,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "room": self.room,
            "description": self.description
        }
        return arr

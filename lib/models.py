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

    def __init__(self):
        pass

class Course:

    code = ""
    name = ""
    lessons = [] # list of Lesson objects

    def __init__(self, code, name=""):
        self.code = code
        self.name = name

class Lesson:

    startPeriod = 0     # starting period
    endPeriod = 0       # ending period
    startWeek = 0       # starting week
    endWeek = 0         # ending week
    dayOfWeek = None    # Day enum
    startTime = 0       # starting hour
    endTime = 0         # ending houd
    room = None         # room name or number

from django.db import models
import json

# ------------------------------------------------------------------------------
# Name:        models.py
# Purpose:     Contains all models in this app
#
# Author:      Matias
#
# Created:     25.09.2015
# Copyright:   (c) Matias 2015
# ------------------------------------------------------------------------------


class Link:

    name = ""
    url = ""

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return (self.name + "\n " + self.url)

class LessonType(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class Period(models.Model):
    # period number on normal periods,
    # week number on intensive courses
    number = models.SmallIntegerField()
    
    # period type, can be "Intensive" or "Normal". Default is "None"
    type = models.CharField(max_length=10)
    
    def __str__(self):
        return ""
        #return self.type
    

class Schelude(models.Model):

    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    #needs to be reworked
    """
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
    """

class Course(models.Model):

    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    schelude = models.ForeignKey(Schelude)
    
    def __str__(self):
        return self.name + " - " + self.code
    
    
    def getLessons(self):
        return Lesson.objects.filter(course=self.pk)
        
    
    def lessonsTable(self):
        lessons = self.getLessons()
        
        if (len(lessons) == 0):
            return ""
        
        tableHTML = '<table class="table table-hover table-bordered table-condensed">'
        tableHTML += lessons[0].tableHeaders()
        for lesson in lessons:
            tableHTML += lesson.tableRow()
        tableHTML += "</table>"
        
        return tableHTML
        
    # needs to be reworked!!!
    """
    def __str__(self):
        r = ""
        r += "Course name: {0}\n".format(self.name)
        r += "Course code: {0}\n".format(self.code)
        r += "Lessons: \n"
        for lesson in self.lessons:
            r += lesson.__str__(2)
            r += "\n"

        return r

    
    
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
    """

class Lesson(models.Model):

    lessonType = models.ForeignKey(LessonType)
    period = models.ManyToManyField(Period)
    week = models.CharField(max_length=200, blank=True, null=True)
    dayOfWeek = models.CharField(max_length=200, blank=True, null=True)
    startTime = models.TimeField(null=True)
    endTime = models.TimeField(null=True)
    room = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    course = models.ForeignKey(Course, null=True)
    

    def strAll(self, indent=0):
        r = ""
        r += "{1}Name: {0}\n".format( self.name, " "*indent )
        r += "{1}Type: {0}\n".format( self.lessonType, " "*indent )
        r += "{1}Period: {0}\n".format( self.period, " "*indent )
        r += "{1}Weeks: {0}\n".format( self.week, " "*indent )
        r += "{1}Day: {0}\n".format( self.dayOfWeek, " "*indent )
        r += "{1}Starts: {0}\n".format( self.startTime, " "*indent )
        r += "{1}Ends: {0}\n".format( self.endTime, " "*indent )
        r += "{1}Lecture hall: {0}\n".format( self.room, " "*indent )
        r += "{1}Description: {0}\n".format( self.description, " "*indent )

        return r
        
    
    # for templates
    def tableHeaders(self):
        r = "<tr>"
        r += "<th>{0}</th>".format( "Name" )
        r += "<th>{0}</th>".format( "Type" )
        r += "<th>{0}</th>".format( "Period" )
        r += "<th>{0}</th>".format( "Weeks" )
        r += "<th>{0}</th>".format( "Day" )
        r += "<th>{0}</th>".format( "Starts" )
        r += "<th>{0}</th>".format( "Ends" )
        r += "<th>{0}</th>".format( "Room" )
        r += "<th>{0}</th>".format( "Description" )
        r += "</tr>"
        
        return r
    
    
    # for templates
    def tableRow(self):
        #per = self.period
        per = ""
        r = "<tr>"
        r += "<td>{0}</td>".format( self.name )
        r += "<td>{0}</td>".format( self.lessonType )
        r += "<td>{0}</td>".format( per )
        r += "<td>{0}</td>".format( self.week )
        r += "<td>{0}</td>".format( self.dayOfWeek )
        r += "<td>{0}</td>".format( self.startTime )
        r += "<td>{0}</td>".format( self.endTime )
        r += "<td>{0}</td>".format( self.room )
        r += "<td>{0}</td>".format( self.description )
        r += "</tr>"
        
        return r
    
        
    def __str__(self):
        return self.name
        

    # needs to be reworked!!!!
    """
    def toDict(self):
        arr = {
            "lessonType": self.lessonType,
            "period": self.period,
            "week": self.week,
            "dayOfWeek": self.dayOfWeek,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "room": self.room,
            "description": self.description,
            "name": self.name
        }
        return arr
    """
    
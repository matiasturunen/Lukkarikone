from django.db.models import Q
from main.models import LessonType, Period, Schelude, Course, Lesson

def findCourseByName(name="", code="", scheludeIds=[]):
    
    if (len(scheludeIds) == 0):
        scheludeIds = Schelude.objects.values_list("id", flat=True)
    
    c = Course.objects.filter(
        Q( name__icontains=name ),
        Q( code__icontains=code ),
        Q( schelude__in=scheludeIds )
    )
    return c
    
    
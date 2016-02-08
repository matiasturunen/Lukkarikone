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
    
    
def findCourseAdvanced(name="", code="", scheludeIds=[], room="", periods=[], 
                        lessontypes=[], week="", start_hour="", end_hour=""):
                            
    print (scheludeIds)
                            
    if (len(scheludeIds) == 0):
        scheludeIds = Schelude.objects.values_list("id", flat=True)
        
    if (len(periods) == 0):
        periods = Period.objects.values_list("id", flat=True)

    if (len(lessontypes) == 0):
        lessontypes = LessonType.objects.values_list("id", flat=True)
    
    print (scheludeIds)
    lessons = Lesson.objects.filter(
        Q( course__name__icontains=name ),
        Q( course__code__icontains=code ),
        Q( course__schelude__in=scheludeIds ),
        Q( room__icontains=room ),
        Q( period__in=periods),
        Q( lessonType__in=lessontypes ),
        Q( week__contains=week ),
        #Q( startTime ... )
        #Q( endTime ... )
    ).order_by("course__name")
    
    return lessons
        
    
    
from django.contrib import admin
from .models import LessonType, Period, Schelude, Course, Lesson

admin.site.register(LessonType)
admin.site.register(Period)
admin.site.register(Schelude)
admin.site.register(Course)
admin.site.register(Lesson)

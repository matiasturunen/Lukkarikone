from django import forms
from main.models import *

class SimpleSearchForm(forms.Form):
    
    course_name = forms.CharField(
        label='Course name', 
        max_length=100,
        widget=forms.TextInput(attrs={ 
            "class": "form-control",
            "placeholder": "Course name"
        })
    )
    course_code = forms.CharField(
        label='Course code',
        max_length=20,
        widget=forms.TextInput(attrs={ 
            "class": "form-control",
            "placeholder": "Course code"
        })
    )


class AdvancedSearchForm(forms.Form):
    

    scheludes = forms.ModelChoiceField(
        label='Schelude name', 
        queryset=Schelude.objects.all().order_by('name'),
        widget=forms.Select(attrs={ 
            "class": "form-control"
        })
    )
    
    course_name = forms.CharField(
        label='Course name', 
        max_length=100,
        widget=forms.TextInput(attrs={ 
            "class": "form-control",
            "placeholder": "Course name"
        })
    )
    
    course_code = forms.CharField(
        label='Course code',
        max_length=20,
        widget=forms.TextInput(attrs={ 
            "class": "form-control",
            "placeholder": "Course code"
        })
    )
    
    room_number = forms.CharField(
        label='Room number',
        max_length=20,
        widget=forms.TextInput(attrs={ 
            "class": "form-control",
            "placeholder": "Room number"
        })
    )
    
    period_number = forms.ModelChoiceField(
        label='Period number',
        queryset=Period.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )
    
    lesson_type = forms.ModelChoiceField(
        label='Lesson type',
        queryset=LessonType.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )
    
    week_number = forms.ChoiceField(
        label="Week number",
        choices=[(x,x) for x in range(1,53)],
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )
    
    start_hour = forms.ChoiceField(
        label="Starting hour",
        choices=[(x,x) for x in range(0,24)],
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )
    
    end_hour = forms.ChoiceField(
        label="Ending hour",
        choices=[(x,x) for x in range(0,24)],
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )
    
    
from django import forms
from main.models import Schelude

class SimpleSearchForm(forms.Form):
    
    """ Disabled
    scheludes = forms.ModelMultipleChoiceField(
        label='Schelude name', 
        queryset=Schelude.objects.all().order_by('name'),
        widget=forms.SelectMultiple(attrs={ 
            "class": "form-control"
        }))
    """
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
from django import forms
from main.models import Schelude

class SimpleSearchForm(forms.Form):
    scheludes = forms.ModelMultipleChoiceField(label='Schelude name', queryset=Schelude.objects.all().order_by('name'))
    course_name = forms.CharField(label='Course name', max_length=100)
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import SimpleSearchForm, AdvancedSearchForm
from .search import finder
from .models import Lesson


def indexView(request):
    template_name = 'main/index.html'
    return render(request,template_name)
    

def searchAdvancedView(request):
    # advanced search view / form with more options
    # all possible fields
    template_name = 'main/search_advanced.html'
    
    form = AdvancedSearchForm()
    if (request.method == "POST"):
        form = AdvancedSearchForm(request.POST)
        if (form.is_valid):
            
            form_scheludes = [request.POST["scheludes"]]
            if (form_scheludes[0] == ""):
                form_scheludes = []
                
            form_periods = [request.POST["period_number"]]
            if (form_periods[0] == ""):
                form_periods = []
                
            form_lessontypes = [request.POST["lesson_type"]]
            if (form_lessontypes[0] == ""):
                form_lessontypes = []
            
            results = finder.findCourseAdvanced(
                name=request.POST["course_name"], 
                code=request.POST["course_code"],
                scheludeIds=form_scheludes,
                room=request.POST["room_number"],
                #periods=[form_periods],
                #lessontypes=[form_lessontypes]
            )

            return render(request, 
                template_name, {
                'form': form,
                'errors': [],
                'results': results,
            })
        
    errors = form.errors or None
    
    return render(request, 
        template_name, {
        'form': form,
        'errors': errors,
    })
    
    
    
def searchResultView(request):
    # display search results
    # 
    return HttpResponse("None")
    

def searchSimpleScheludes(request):
    # do simple searching
    # search options in POST
    
    template_name = 'main/search.html'
    
    form = SimpleSearchForm()
    if request.method == "POST":
        form = SimpleSearchForm(request.POST)
        if form.is_valid:
            
            results = finder.findCourseByName(
                request.POST["course_name"], 
                request.POST["course_code"]
            )

            return render(request, 
                template_name, {
                'form': form,
                'errors': [],
                'results': results,
            })
        
    errors = form.errors or None # form not submitted or it has errors
    return render(request, 
        template_name, {
        'form': form,
        'errors': errors,
    })
    
    


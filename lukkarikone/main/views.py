from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import SimpleSearchForm
from .search import finder
from .models import Lesson


def indexView(request):
    template_name = 'main/index.html'
    return render(request,template_name)
    

def searchAdvancedView(request):
    # advanced search view / form with more options
    # all possible fields
    template_name = 'main/search_advanced.html'
    return render(request, template_name)
    
    
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
            asd=""
            
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
    
    


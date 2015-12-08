from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import SimpleSearchForm
from .search import finder


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
    
    form = SimpleSearchForm()
    if request.method == "POST":
        form = SimpleSearchForm(request.POST)
        if form.is_valid:
            asd=""
            
            result = finder.findCourseByName(
                request.POST["course_name"], 
                request.POST["course_code"], 
                request.POST.getlist("scheludes")
            )
            for x in result:
                asd+="<br>"+x.__str__()
            return HttpResponse("searched!!" + asd) 
        
    errors = form.errors or None # form not submitted or it has errors
    return render(request, 
        'main/search.html', {
        'form': form,
        'errors': errors,
    })
    
    


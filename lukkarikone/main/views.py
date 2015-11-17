from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import SimpleSearchForm


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
            #redirect to the url where you'll process the input
            return HttpResponse("searched!!") # insert reverse or url
        
    errors = form.errors or None # form not submitted or it has errors
    return render(request, 
        'main/search.html', {
        'form': form,
        'errors': errors,
    })
    
    


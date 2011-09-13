from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.http import Http404

from feedeater.models import Feed, Entry

def feedeater_interactive(request):
    ''' Allows one to search and sort the results from Feedeater '''
    pass

def recent_entries(request):
    ''' Show 10 most recent items '''
    recent_entries = Entry.objects.all().order_by('-posted_on')[0:10]
    return render_to_response("basic.html",
            { 'recent_entries': recent_entries },
            context_instance=RequestContext(request),
        )

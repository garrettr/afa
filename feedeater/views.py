from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.core import serializers
from django.db.models import Q

from feedeater.models import Feed, Entry

def search(request):
    ''' Renders basic search template - start with 10 most recent posts '''
    recent_entries = Entry.objects.all().order_by('-posted_on')[0:10]
    return render_to_response("feedeater/search.html",
            { 'recent_entries': recent_entries },
            context_instance=RequestContext(request),
        )

def search_ajax(request):
    ''' Processes AJAX requests from search view '''
    reply = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        q = request.GET.get('q', '')
        # build queryset
        qs = build_search_queryset(
                q, 
                ['title', 'content', 'feed__title',]
            )
        if( request.GET.get('so', '') == 'asc' ):
            found_entries = Entry.objects.filter(qs).order_by('posted_on')
        else: # default to desc. order (newest first)
            found_entries = Entry.objects.filter(qs).order_by('-posted_on')
        # all_objects = list(found_entries) + list(Feed.objects.all())
        j = serializers.get_serializer("json")()
        json = j.serialize(found_entries, ensure_ascii=False,
                use_natural_keys=True)
        return HttpResponse(json, mimetype='application/json')

def build_search_queryset(query_string, search_fields):
    '''
    Returns queryset that searchs over given fields
    for every term in query_string

    Thanks to http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
    '''
    query = None # Query that searches for every search term

    terms = query_string.split()
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name : term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query # AND's search terms by default

    return query

def recent_entries(request):
    '''
    Returns list of entries, most recent first
    Hard-coding 5 entries (for now)
    '''
    if len(Feed.objects.all()) > 5:
        # return most recent entry from each feed
        all_recent = Entry.objects.order_by('-posted_on')
    else:
        # return 5 most recent
        recent_entries = Entry.objects.order_by('-posted_on')
    return render_to_response("feedeater/recent_entries.html",
            { 'recent_entries': recent_entries },
            context_instance=RequestContext(request),
        )

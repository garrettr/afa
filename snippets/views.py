from django.shortcuts import render_to_response
from django.template import RequestContext

from snippets.models import Snippet

import random

def random_snippet(request):
    '''
    Picks a random snippet and renders it as a template
    '''
    num_snippets = len(Snippet.objects.all())
    # randint(a,b) returns N s.t. a <= N <= b
    if num_snippets > 0:
        index_pick = random.randint(0, num_snippets-1)
        snippet = Snippet.objects.all()[index_pick]
    else:
        snippet = None
    return render_to_response("snippets/snippet.html",
            { 'snippet': snippet },
            context_instance=RequestContext(request),
        )

def all_as_gallery(request):
    '''
    Returns all snippets in a list
    so they can be rendered in a gallery with slides.js
    '''
    snippets = Snippet.objects.all()
    return render_to_response("snippets/all_as_gallery.html",
            { 'snippets': snippets },
            context_instance=RequestContext(request),
        )

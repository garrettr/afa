from django import template
from feedeater.models import Entry

def do_latest_entries(parser, token):
    return LatestEntriesNode()

class LatestEntriesNode(template.Node):
    def render(self, context):
        context['latest_entries'] = Entry.objects.all().order_by('-posted_on')
        return ''

register = template.Library()
register.tag('get_latest_entries', do_latest_entries)

from django.core.management.base import BaseCommand, CommandError
from feedeater.models import Entry, Feed

class Command(BaseCommand):
    args = 'none'
    help = '''
    Checks all feeds for updates;
    downloads and saves as Entries any that it finds.
    '''

    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        for f in feeds:
            print "Updating %s..." % f.title
            f.update_entries()
        print "Done."

from django.core.management.base import BaseCommand, CommandError
from feedeater.models import Entry, Feed

import mylogging as LOG

class Command(BaseCommand):
    args = 'none'
    help = '''
    Checks all feeds for updates;
    downloads and saves as Entries any that it finds.
    '''

    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        for f in feeds:
            LOG.debug("Updating %s..." % f.title)
            f.update_entries()
        LOG.debug("Done.")

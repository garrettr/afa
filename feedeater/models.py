from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
import re
import feedparser
import twitter
import rfc822   # for parsing Twitter's dates
from settings import FACEBOOK_APP_ID, FACEBOOK_APP_TOKEN
# using the idea from http://stackoverflow.com/questions/2690723/facebook-graph-api-and-django
from urllib2 import urlopen
from simplejson import loads

class Entry(models.Model):
    """
    Represents a single entry in a feed
    """
    feed = models.ForeignKey("Feed", related_name="entries")
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    content = models.TextField()

    posted_on = models.DateTimeField(_('posted on'))
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    
    class Meta:
        ordering=['-posted_on']
        verbose_name_plural = "Entries"

    def __unicode__(self):
        return u'%s, from %s' % (self.title, self.feed.title)

class Feed(models.Model):
    """
    Represents a social media feed via a url
    """
    title = models.CharField(max_length=140,
        help_text="A descriptive name for this feed")
    url = models.URLField(help_text="Enter a specific URL")

    SOURCE_CHOICES = (
        (u'FB', u'Facebook'),
        (u'TW', u'Twitter'),
        (u'RA', u'RSS/Atom'),
    )
    source = models.CharField(max_length=2, choices=SOURCE_CHOICES)
    
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    # should reflect last time we pulled something new?
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __unicode__(self):
        return u'%s : %s' % (self.title, self.get_source_display())

    def update_entries(self):
        '''
        Copy all entries not saved to the database
        Call on first model save to populate, and then again with cron job
        '''
        if self.source == 'FB':
            # GET https://graph.facebook.com/oauth/access_token?client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&grant_type=client_credentials
            # Returns access_token= in body of response.
            # Now we can access a Page's wall like this:
            # https://graph.facebook.com/pagename/feed?access_token=...
            # returns JSON
            # "data": [ list of posts to the wall]
            # -> message, picture, created_time
            # authenticate
            req = "https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials" % (FACEBOOK_APP_ID, FACEBOOK_APP_TOKEN)
            token_request = urlopen(req).read()
            access_token = token_request[len("access_token="):] # token_request is "access_token=xxx..."
            fbregx = re.match(
                    r'(https?://www.facebook.com/)?(?P<fbid>[a-zA-Z0-9\.]{5,})',
                    self.url)
            fbid = fbregx.group('fbid')
            feed_url = "https://graph.facebook.com/%s/feed?access_token=%s" % (fbid, access_token)
            feed = loads(urlopen(feed_url).read())

            sorted_entries = self.entries.order_by('-posted_on') # https://docs.djangoproject.com/en/1.3/topics/db/queries/#following-relationships-backward
            if sorted_entries:
                # get most recent saved post
                mr_saved = sorted_entries[0]
                for post in feed['data']:
                    post_time = datetime.striptime(
                        post['created_time'],
                        "%Y-%m-%dT%H:%M:%S+0000"
                    )
                    if post_time <= mr_saved.posted_on:
                        # we've reached what's already been saved
                        # NOTE: this assumes the input is sorted
                        break
                    else:
                        # a new one! save it
                        post_id = post['id'].split("_")[1]
                        purl = "%s/posts/%s" % (self.url, post_id)
                        try:
                            e = Entry(
                                    feed=self,
                                    title=post['name'],
                                    url=purl,
                                    content=post['message'],
                                    # example:
                                    # "created_time": "2011-07-20T19:49:17+0000"
                                    posted_on=datetime.strptime(
                                        post['created_time'],
                                        "%Y-%m-%dT%H:%M:%S+0000"
                                    )
                                )
                            e.save()
                        except KeyError:
                            # sometimes there isn't a message param - I guess if it's
                            # just a photo
                            pass
            else:
                # this is the initial save - populate with all entries
                for post in feed['data']:
                    # data is a list of dictionaries, each describing a feed post
                    # each posts id is of the format pageid_postid
                    post_id = post['id'].split("_")[1]
                    purl = "%s/posts/%s" % (self.url, post_id)
                    try:
                        e = Entry(
                                feed=self,
                                title=post['name'],
                                url=purl,
                                content=post['message'],
                                # example:
                                # "created_time": "2011-07-20T19:49:17+0000"
                                posted_on=datetime.strptime(
                                    post['created_time'],
                                    "%Y-%m-%dT%H:%M:%S+0000"
                                )
                            )
                        e.save()
                    except KeyError:
                        # sometimes there isn't a message param - I guess if it's
                        # just a photo
                        pass

        elif self.source == 'TW':
            # Create an instance of the Twitter API with no-auth
            # no authentication needed for public timelines
            api = twitter.Api()
            # match against this regex
            # accepts http(s) full twitter url or just username
            # seems like we should probably only allow full url - we use it for
            # it's urlness later on
            tregx = re.match(
                    r'(https?://twitter.com/#!/){0,1}(?P<tid>[a-zA-Z0-9_]{1,15})',
                    self.url)
            tid = tregx.group('tid')
            statuses = api.GetUserTimeline(tid)

            sorted_entries = self.entries.order_by('-posted_on')
            if sorted_entries:
                # get most recent saved post
                mr_saved = sorted_entries[0]
                for status in statuses:
                    post_time = datetime(*rfc822.parsedate(status.created_at)[:6])
                    if post_time <= mr_saved.posted_on:
                        break
                    else:
                        status_url = "%s/status/%s" % (self.url, status.id)
                        e = Entry(
                                feed=self,
                                title=status.text,
                                url=status_url,
                                content=status.text,
                                posted_on=datetime(*rfc822.parsedate(status.created_at)[:6])
                            )
                        e.save()
            else:
                # first model save - populate with all entries
                for status in statuses:
                    # build individual tweet URL
                    # subject to change based on Twitter's URL scheme
                    # worry about the first slash later
                    # they will still work, just look bad
                    status_url = "%s/status/%s" % (self.url, status.id)
                    e = Entry(
                            feed=self,
                            title=status.text,
                            url=status_url,
                            content=status.text,
                            posted_on=datetime(*rfc822.parsedate(status.created_at)[:6])
                        )
                    e.save()

        elif self.source == 'RA':
            d = feedparser.parse(self.url)
            # download everything and save it
            sorted_entries = self.entries.order_by('-posted_on')
            if sorted_entries:
                # get most recent saved post
                mr_saved = sorted_entries[0]
                for post in d.entries:
                    post_time = datetime(*post.updated_parsed[:6])
                    if post_time <= mr_saved.posted_on:
                        break   # NOTE: this assumes the input is sorted
                    else:
                        e = Entry(
                                feed=self,
                                title=post.title,
                                url=post.link,
                                content=post.summary,
                                posted_on=datetime(*post.updated_parsed[:6])
                            )
                        e.save()
            else:
                # first save - populate with all entries
                for post in d.entries:
                    e = Entry(
                            feed=self,
                            title=post.title,
                            url=post.link,
                            content=post.summary,
                            posted_on=datetime(*post.updated_parsed[:6])
                        )
                    e.save()

        else:
            print "I don't recognize that source type."
            # This should never happen - handle properly later

    def save(self, *args, **kwargs):
        super(Feed, self).save(*args, **kwargs)
        self.update_entries()

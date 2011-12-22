from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.core.files import File
from django.core.files.base import ContentFile

from datetime import datetime
import re
import os
import StringIO
import feedparser
import twitter
import rfc822   # for parsing Twitter's dates
from django.conf import settings
# using the idea from http://stackoverflow.com/questions/2690723/facebook-graph-api-and-django
from urllib2 import urlopen
from urlparse import urlparse
from simplejson import loads

#import mylogging as LOG

FACEBOOK_APP_ID = settings.FACEBOOK_APP_ID
FACEBOOK_APP_TOKEN = settings.FACEBOOK_APP_TOKEN

class Entry(models.Model):
    """
    Represents a single entry in a feed
    """
    feed = models.ForeignKey("Feed", related_name="entries")
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
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
    url = models.CharField(max_length=500, unique=True,
            help_text="Enter the URL of a Facebook Page, Twitter Page, or RSS/Atom Feed")
    image = models.ImageField(upload_to="feedeater/", blank=True,
            editable=True, default=None)

    SOURCE_CHOICES = (
        (u'FB', u'Facebook'),
        (u'TW', u'Twitter'),
        (u'RA', u'RSS/Atom'),
    )
    source = models.CharField(max_length=2, choices=SOURCE_CHOICES,
            editable=False)
    
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    # should reflect last time we pulled something new?
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.title)

    # Do this for now: it works, but a full serialization solution would be
    # nicer. Here's an option: http://code.google.com/p/wadofstuff/wiki/DjangoFullSerializers
    def natural_key(self):
        return (self.title, self.url, self.source, self.image.name)

    def _update_facebook(self):
        '''
        Update self with the Facebook API
        '''
        # authenticate
        req = ("https://graph.facebook.com/oauth/access_token?"
               "client_id=%s&client_secret=%s&grant_type=client_credentials"
               % (FACEBOOK_APP_ID, FACEBOOK_APP_TOKEN))
        token_request = urlopen(req).read()
        access_token = token_request[len("access_token="):] # token_request is "access_token=xxx..."
        if "/pages/" in self.url:
            # old-style page URL uses numeric id:
            # http://www.facebook.com/pages/username/id
            fbregx = re.match(
                    r"(https?://www.facebook.com/pages/"
                     "[a-zA-Z0-9\.]+/)?(?P<fbid>[0-9]+)",
                    self.url)
        else:
            # if the page has a username set, it can be accessed with it
            # http://www.facebook.com/usernmame
            fbregx = re.match(
                    r"(https?://www.facebook.com/)?"
                     "(?P<fbid>[a-zA-Z0-9\.]{5,})",
                    self.url)
        fbid = fbregx.group('fbid')
        feed_url = ("https://graph.facebook.com/"
                    "%s/feed?access_token=%s"
                    % (fbid, access_token))
        feed = loads(urlopen(feed_url).read())

        try:
            most_recent_saved = self.entries.order_by('-posted_on')[0]

            for post in feed['data']:
                post_time = datetime.strptime(
                    post['created_time'],
                    "%Y-%m-%dT%H:%M:%S+0000"
                )
                if post_time <= most_recent_saved.posted_on:
                    break
                else:
                    post_id = post['id'].split("_")[1]
                    purl = "%s/posts/%s" % (self.url, post_id)
                    try:
                        e = Entry(
                                feed=self,
                                title=post['name'],
                                url=purl,
                                content=strip_tags(post['message']),
                                posted_on=datetime.strptime(
                                    post['created_time'],
                                    "%Y-%m-%dT%H:%M:%S+0000"
                                )
                            )
                        e.save()
                    except KeyError:
                        pass # some post types have no message key
        except IndexError: # no Entry saved yet
            for post in feed['data']:
                # post['id'] = pageid_postid
                post_id = post['id'].split("_")[1]
                purl = "%s/posts/%s" % (self.url, post_id)
                try:
                    e = Entry(
                            feed=self,
                            title=post['name'],
                            url=purl,
                            content=strip_tags(post['message']),
                            posted_on=datetime.strptime(
                                post['created_time'],
                                "%Y-%m-%dT%H:%M:%S+0000"
                            )
                        )
                    e.save()
                except KeyError:
                    pass

    def _update_twitter(self):
        # No authentication needed for public timelines
        api = twitter.Api()
        # accepts http(s) full twitter url or just username
        tregx = re.match(
                r'(https?://twitter.com/#!/){0,1}(?P<tid>[a-zA-Z0-9_]{1,15})',
                self.url)
        tid = tregx.group('tid')
        tweets = api.GetUserTimeline(tid)

        try:

            most_recent_saved = self.entries.order_by('-posted_on')[0]

            for tweet in tweets:
                post_time = datetime(*rfc822.parsedate(tweet.created_at)[:6])
                if post_time <= most_recent_saved.posted_on:
                    break
                else:
                    try:
                        e = Entry(
                                feed=self,
                                title=tweet.text,
                                url="%s/status/%s" % (self.url, tweet.id),
                                content=strip_tags(tweet.text),
                                posted_on=post_time
                            )
                        e.save()
                    except KeyError:
                        pass
                    
        except IndexError: # no Entry saved yet

            for tweet in tweets:
                post_time = datetime(*rfc822.parsedate(tweet.created_at)[:6])
                e = Entry(
                        feed=self,
                        title=tweet.text,
                        url="%s/status/%s" % (self.url, tweet.id),
                        content=strip_tags(tweet.text),
                        posted_on=post_time
                    )
                e.save()

    def _update_rssatom(self):
        d = feedparser.parse(self.url)
        try:
            most_recent_saved = self.entries.order_by('-posted_on')[0]

            for post in d.entries:
                post_time = datetime(*post.updated_parsed[:6])
                if post_time <= most_recent_saved.posted_on:
                    break
                else:
                    e = Entry(
                            feed=self,
                            title=post.title,
                            url=post.link,
                            content=strip_tags(post.summary),
                            posted_on=datetime(*post.updated_parsed[:6])
                        )
                    e.save()

        except IndexError: # no Entry saved
            for post in d.entries:
                e = Entry(
                        feed=self,
                        title=post.title,
                        url=post.link,
                        content=strip_tags(post.summary),
                        posted_on=datetime(*post.updated_parsed[:6])
                    )
                e.save()

    def update_entries(self):
        '''
        Copy all entries not saved to the database
        Call on first model save to populate, and then again with cron job
        '''
        if self.source == 'FB':
            self._update_facebook()
        if self.source == 'TW':
            self._update_twitter()
        if self.source == 'RA':
            self._update_rssatom()

    def _get_source(self):
        '''
        Given a URL, attempt to return the source
        '''
        if "twitter.com/" in self.url:
            return 'TW'
        elif "facebook.com/" in self.url:
            return 'FB'
        else: # default try to process as RSS/Atom
            return 'RA'

    def _get_image(self):
        '''
        Given a URL and source type, try to get an image to associate, save it,
        and set the image field
        '''
        image_url = None
        if self.source == 'FB':
            if "/pages/" in self.url:
                fbregx = re.match(
                        r'(https?://www.facebook.com/pages/[a-zA-Z0-9\.]+/)?(?P<fbid>[0-9]+)',
                        self.url)
            else:
                fbregx = re.match(
                        r'(https?://www.facebook.com/)?(?P<fbid>[a-zA-Z0-9\.]{5,})',
                        self.url)
            fbid = fbregx.group('fbid')
            image_url = "https://graph.facebook.com/%s/picture" % (fbid)
        elif self.source == 'TW':
            api = twitter.Api()
            tregx = re.match(
                    r'(https?://twitter.com/#!/){0,1}(?P<tid>[a-zA-Z0-9_]{1,15})',
                    self.url)
            tid = tregx.group('tid')
            user = api.GetUser(tid)
            image_url = user.profile_image_url
        elif self.source == 'RA':
            self.image = None # or set to a default?
            return
        
        image_data = urlopen(image_url)
        filename = urlparse(image_data.geturl()).path.split('/')[-1]
        self.image = filename
        self.image.save(
            filename,
            ContentFile(image_data.read()),
            save=False
            )

    def save(self, *args, **kwargs):
        self.source = self._get_source()
        self._get_image()
        super(Feed, self).save(*args, **kwargs)
        self.update_entries()

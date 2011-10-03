from django.core.management.base import BaseCommand, CommandError
from news.models import Post

from django.core.files import File
from django.conf import settings
from feincms.module.medialibrary.models import MediaFile

import sys, os
import imaplib
import email
import mimetypes

NEWS_HOSTNAME = ''
NEWS_ACCOUNT = ''
NEWS_PASSWORD = ''
NEWS_MAILBOX = ''

from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime

import mylogging as LOG

def open_connection(hostname, account, password, verbose=False):
    # Connect to the server
    LOG.debug('Connecting to %s' % hostname)
    connection = imaplib.IMAP4_SSL(hostname)
    connection.login(account, password)
    return connection

def process_email(msg):
    # verify the sender is an admin
    # get all users that can login to the admin
    users = User.objects.filter(is_staff=True)
    from_user = None
    for user in users:
        # note that the from field might be of the form
        # name <email@domain>
        # so we'll see if user.email is in the from field
        # also, '' is in any string, so make sure the user specified
        # an email first
        if user.email and user.email in msg['from']:
            from_user = user # do a posted_by?
    # not an allowed e-mail? for now, return (ignore)
    if not from_user:
        LOG.warning('Got an email from a non-staff member: %s. Ignored.' % msg['from'])
        return

    # parse message; walk through structure
    body = []
    attachments = []
    for part in msg.walk():
        LOG.debug('Found content_type: %s' % part.get_content_type())
        mtype = part.get_content_maintype()
        if mtype == 'text' or mtype == 'message':
            body.append(part)
        if mtype == 'image' or mtype == 'video' or mtype == 'audio' or mtype == 'application':
            # consider security risks
            attachments.append(part)

    # debugging
    LOG.debug('body[]: %s' % body)
    LOG.debug('attachments[]: %s' % attachments)

    # if text/html exists, use it
    body_text = [p.get_payload() for p in body if p.get_content_type() == 'text/html']
    if not body_text:
        # default to 'text/plain'
        body_text = [p.get_payload() for p in body if p.get_content_type() == 'text/plain']
    body_text = body_text[0]

    # process attachments
    counter = 1
    media_files = []
    for attachment in attachments:
        # create a mediafile, save it
        filename = attachment.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(attachment.get_content_type())
            if not ext:
                # Use generic extension
                ext = '.bin'
            filename = 'part-%03d%s' % (counter, ext)
        counter += 1
        # save intermediate file to tmp
        fpath = os.path.join(os.path.join
                (settings.MEDIA_ROOT, 'news_uploads'),
                filename)
        with open(fpath, 'wb') as fp:
            fp.write(attachment.get_payload(decode=True))
        with open(fpath, 'rb') as fp:
            m = MediaFile(file = File(fp))
            m.save()
            media_files.append(m)

    post_photo = None
    for mf in media_files:
        if mf.type == 'image':  # grab the first attached image
            post_photo = mf
            break

    p = Post(
            headline=msg['subject'],
            slug=slugify(msg['subject']),
            body = body_text, # should strip tags from this
            photo = post_photo,
            pub_date = datetime.now(),
        )
    p.save()
    p.media_files.add(*media_files)
    p.save()

class Command(BaseCommand):
    args = 'none'   # or maybe account name, password
    help = '''
    Checks given e-mail account for new mail.
    If found, add as a post, then delete.
    '''

    def handle(self, *args, **options):
        try:
            # open connection to IMAP server
            c = open_connection(hostname=settings.NEWS_HOSTNAME,
                    account=settings.NEWS_ACCOUNT,
                    password=settings.NEWS_PASSWORD,
                    verbose=True)
            LOG.debug('Connection: %s' % c)
            # open the mailbox
            typ, data = c.select(settings.NEWS_MAILBOX) # should be a variable?
            LOG.debug('Opening mailbox: %s' % settings.NEWS_MAILBOX)
            # number of messages in the mailbox
            num_msgs = int(data[0])
            # search for unseen messages
            typ, msg_ids = c.search(None, '(UNSEEN)')
            if msg_ids != ['']: # if there are unseen msgs
                # fetch wants ids with commas, like 1,2,3
                mids = ','.join(msg_ids[0].split(' '))
                # note - this fetch makes all msgs SEEN
                typ, msg_data = c.fetch(mids, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        for header in ['subject', 'to', 'from']:
                            LOG.debug('Unread E-mail:\n%-8s %s' %
                                    (header.upper(), msg[header])
                                )
                        process_email(msg)
        finally:
            try:
                c.close()
                c.logout()
            except:
                LOG.warning("Something went wrong closing the connection/logging out.")
                pass

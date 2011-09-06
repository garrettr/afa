from django.core.management.base import BaseCommand, CommandError
from news.models import Post

import imaplib
import email

NEWS_HOSTNAME = ''
NEWS_ACCOUNT = ''
NEWS_PASSWORD = ''
NEWS_MAILBOX = ''

from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime

def open_connection(hostname, account, password, verbose=False):
    # Connect to the server
    print 'Connecting to', hostname
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
        return

    # get the body of the email
    #body = ''
    #if msg.is_multipart():
    #    print "msg is multipart"
    #    html_pl = [p for p in msg.get_payload() if p.get_content_type() == 'text/html']
    #    if html_pl:
    #        body = html_pl[0]
    #    else:
    #        # no html text in the email; get the default
    #        df_pl = [p for p in msg.get_payload() if p.get_content_type() == 'text/plain']
    #        body = df_pl[0]
    #else:
    #    print "msg is not multipart"
    #    body = msg.get_payload()

    # remove header from body
    # 
    # better way - walk through message strucutre
    body = []
    attachments = []
    for part in msg.walk():
        print part.get_content_type()
        mtype = part.get_content_maintype()
        if mtype == 'text' or mtype == 'message':
            body.append(part)
        if mtype == 'image' or mtype == 'video' or mtype == 'audio' or mtype == 'application':
            # consider security risks
            attachments.append(part)

    # if text/html exists, use it
    body_text = [p.get_payload() for p in body if p.get_content_type() == 'text/html']
    if not body_text:
        body_text = [p.get_payload() for p in body if p.get_content_type() == 'text/plain']
    # strip headers (first 3 lines)
    body_text = '\n'.join(body_text[0].split('\n')[2:])
    print body_text

    # process attachments
    if attachments:
        pass

    post_photo = None
    # media_files?

    p = Post(
            headline=msg['subject'],
            slug=slugify(msg['subject']),
            body = body_text, # should strip tags from this
            photo = post_photo,
            pub_date = datetime.now(),
        )
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
            print c
            # open the mailbox
            typ, data = c.select(settings.NEWS_MAILBOX) # should be a variable?
            print "Opening mailbox: ", settings.NEWS_MAILBOX
            print typ, data
            # number of messages in the mailbox
            num_msgs = int(data[0])
            print "num_msgs: ", num_msgs
            # search for unseen messages
            typ, msg_ids = c.search(None, '(UNSEEN)')
            print typ, msg_ids  # msg_ids is a list
            if msg_ids != ['']: # if there are unseen msgs
                # fetch wants ids with commas, like 1,2,3
                mids = ','.join(msg_ids[0].split(' '))
                typ, msg_data = c.fetch(mids, '(RFC822)')
                # note - this fetch applies makes all msgs SEEN
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        for header in ['subject', 'to', 'from']:
                            print '%-8s %s' % (header.upper(), msg[header])
                        process_email(msg)
        finally:
            try:
                c.close()
                c.logout()
            except:
                pass

from django.core.management.base import BaseCommand, CommandError
from news.models import Post

import imaplib
import email
from django.contrib.auth import User

EMAIL_HOSTNAME = ''
ACCOUNT_NAME = ''
ACCOUNT_PASSWORD = ''
MAILBOX_NAME = ''

def open_connection(hostname, account, password, verbose=False):
    # Connect to the server
    print 'Connecting to', hostname
    connection = imaplib.IMAP4_SSL(hostname)
    connection.login(account, password)
    return connection

class Command(BaseCommand):
    args = 'none'   # or maybe account name, password
    help = '''
    Checks given e-mail account for new mail.
    If found, add as a post, then delete.
    '''

    def handle(self, *args, **options):
        try:
            # open connection to IMAP server
            c = open_connection(hostname=EMAIL_HOSTNAME,
                                account=ACCOUNT_NAME,
                                password=ACCOUNT_PASSWORD,
                                verbose=True)
            print c
            # open the mailbox
            typ, data = c.select(MAILBOX_NAME) # should be a variable?
            print typ, data
            # number of messages in the mailbox
            num_msgs = int(data[0])
            # search for unseen messages
            typ, msg_ids = c.search(None, '(UNSEEN)')
            for msg_id in msg_ids:
                typ, msg_data = c.fetch(str(msg_id), '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        for header in ['subject', 'to', 'from']:
                            print '%-8s %s' % (header.upper(), msg[header])
        finally:
            c.close()
            c.logout()

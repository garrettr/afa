"""
Custom wrapper for python logging module

Thanks to http://www.saltycrane.com/blog/2009/10/notes-python-logging/
"""

import logging
import sys

from django.conf import settings

try:
    DEBUG_LOG_FILENAME = settings.DEBUG_LOG_FILENAME
    WARNING_LOG_FILENAME = settings.WARNING_LOG_FILENAME
except AttributeError:
    # just for testing
    DEBUG_LOG_FILENAME = '/tmp/debug.log'
    WARNING_LOG_FILENAME = '/tmp/warning.log'

# set up formatting
formatter = logging.Formatter('[%(asctime)s] %(levelno)s (%(process)d) %(module)s: %(message)s')

# set up logging to STDOUT for all levels DEBUG and higher
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)

# set up logging to a file for all levels DEBUG and higher
fh = logging.FileHandler(DEBUG_LOG_FILENAME)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# set up logging to a file for all levels WARNING and higher
fh2 = logging.FileHandler(WARNING_LOG_FILENAME)
fh2.setLevel(logging.WARN)
fh2.setFormatter(formatter)

# create Logger object
mylogger = logging.getLogger('MyLogger')
mylogger.setLevel(logging.DEBUG)
mylogger.addHandler(sh)
mylogger.addHandler(fh)
mylogger.addHandler(fh2)

# create shortcut functions
debug = mylogger.debug
info = mylogger.info
warning = mylogger.warning
error = mylogger.error
critical = mylogger.critical

README
------

## What?

New website for the Alliance for Appalachia.

## Installation notes

Using the feincms virtualenv for development.

## Dependencies:

### Output of pip freeze (minus leftovers):
Django==1.3
FeinCMS==1.4.1
PIL==1.1.7
distribute==0.6.15
django-mptt==0.5.pre
feedparser==5.0.1
httplib2==0.7.1
oauth2==1.5.170
python-twitter==0.8.2
simplejson==2.1.6
wsgiref==0.1.2

Added accents.py:
/Users/grobinso/Documents/code/virtualenv/python-envs/feincms/lib/python2.6/site-packages/feincms/module/page/extensions/accent.py

This is a FeinCMS Page Extension. I'm keeping it in the repo - there's a symlink from the above path to the file in this git repo.

The following three things are kept in the git repo but should be made accessible elsewhere. I use symlinks.

1.  `news/`
    Put this on your Python path.
2.  `feedeater/`
    likewise
3.  `accent.py`
    is a FeinCMS page extension. To install it, symlink it into `feincms/module/page/extensions/`.
    `ln -s path/to/afa/accent.py path/to/feincms/module/page/extensions`

For now and forever: to make symbolic links, the syntax is: `ln -s <target> <linkname>`

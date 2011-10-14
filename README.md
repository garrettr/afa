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

## Symlinks

The following three things are kept in the git repo but should be made accessible elsewhere. I use symlinks.

1.  `news/`
    Put this on your Python path.
2.  `feedeater/`
    likewise
3.  `snippets/`
    likewise
4.  `accent.py`
    is a FeinCMS page extension. To install it, symlink it into `feincms/module/page/extensions/`.
    `ln -s path/to/afa/accent.py path/to/feincms/module/page/extensions`

For now and forever: to make symbolic links, the syntax is: `ln -s <target> <linkname>`

## Bugs/Todo

RotatingFileHandler - not writing logs anymore, but FileHandler did?
Try `git revert HEAD` (for reverting committed mistakes)
Yup, it's writing logs again. Weird. Work on getting RotatingFileHandler to work.

Error on trying to load OVEC Facebook into feedeater. Something to do with the image.
1 [Fri Oct 07 11:37:03 2011] [error] self.image.name:  feedeater/DSC03250_-_Co
2 [Fri Oct 07 11:45:03 2011] [error] self.image.name:  feedeater/Logo.InD_norm
3 [Fri Oct 07 11:54:22 2011] [error] self.image.name:  feedeater/picture_2
4 [Fri Oct 07 11:54:32 2011] [error] self.image.name:  feedeater/picture_3

# Notes from Katey & others:

GENERAL
--limit entries from one group on social media feed
    done, plus applicationcontent refactor 
--let's just give RAN credit for the video (we also need to give credit for the photos

HOME PAGE
--move explanation of the social media feed to the social media feed section
    make some more snippets (using ILM stuff for example), explain
--change "news" to "around the corner"
    done.

depends on HEADER IMAGE:
--shade entire bridge image
--change color of menus at the top
--eliminate spaces between tabs on top

HOW WE WORK PAGE
--put new drafts in (these were those emails with the conversations of the groups) 
    done
--can we add some images or something to break up the space?

WHAT IS MTR?
--remove photo tag on last image
    = fix captions
    done. double-check what happens if there's no caption. copyright in
    hover text.

RESOURCES
--can we take these down from the live site until we have them?
    unchecked "in navigation" - removes children as well

LINGERING TO-DO AFTERWARD
--Resources Page
--Pay for site
--Update calendar and "around the corner"
--switch domain name


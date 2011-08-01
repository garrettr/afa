README
------

## Why?

Trying a different CMS for the Alliance for Appalachia.
I think they want more flexibility than Mezzanine seems able to provide.

Don't spend too long on this - this is a complete rewrite, and should only be undertaken if you can
get somewhere significant fast. 

## Installation notes

Using the feincms virtualenv for development.

Dependencies:

1. feincms
2. django-mptt
3. PIL
4. django-photologue-2.2

## Todo
Going to try incorporating django-photologue as the image
manipulation/gallery solution.
Configuring django-photologue:

1.  Add 'photologue' to INSTALLED_APPS
2.  syncdb, THEN `python manage.py plinit`
3.  (OPTIONAL) Add photologue urls:
    (r'^photologue/', include('photolgue.urls')), 
4.  Copy templates to templates/photologue



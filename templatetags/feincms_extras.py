from django.template import Library
from feincms.module.medialibrary.models import MediaFile

register = Library()

@register.filter
def width(value):
    '''
    Given an image stored as a FeinCMS mediafile,
    return the image's width
    '''
    if isinstance(value, MediaFile) and value.type == 'image':
        nasty_ft = value.file_type() # "Image x&times;y"
        return int(nasty_ft.split()[1].split("&times;")[0])
    else:
        return 0 # not meaningful if not an image

@register.filter
def height(value):
    '''
    Given an image stored as a FeinCMS mediafile,
    return the image's height
    '''
    if isinstance(value, MediaFile) and value.type == 'image':
        nasty_ft = value.file_type() # "Image x&times;y"
        return int(nasty_ft.split()[1].split("&times;")[1])
    else:
        return 0 # not meaningful if not an image

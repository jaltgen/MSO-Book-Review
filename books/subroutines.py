# -*- coding: utf-8 -*-
"""   subroutines.py

author: Jannik Altgen
contact: jannik.altgen@googlemail.com
since: 2009/08/09
summary: This module is a helper module for the view functions. it sources out frequently used methods, that may be used in various views.

"""
from models import *
from PIL import Image, ImageFilter

def handle_uploaded_file(f):
    destination = open('/srv/static/upload/%s' % (f.name), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    image = Image.open('/srv/static/upload/%s' % (f.name))
    width, height = image.size
    new_size = {}
    #goal format definition
    high_format = {'height':133.0,
                   'width': 100.0}
    wide_format = {'height':100.0,
                   'width': 133.0}
    factor = width/high_format['width']
    new_size['heigth'] = height /int(factor)
    new_size['width'] = width/int(factor)
    
    image = image.filter(ImageFilter.SHARPEN)
    image.thumbnail((int(new_size['width']), int(new_size['heigth']), Image.ANTIALIAS))
    image.save('/srv/static/upload/%s.jpg' % (f.name.split('.')[0]), 'JPEG')
    return "%s.jpg" % (f.name.split('.')[0])

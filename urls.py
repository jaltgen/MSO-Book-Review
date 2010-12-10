# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
#    (r'^$', 'books.views.redirect_to_index'),
    (r'', include("books.books.urls")),
    (r'^admin/(.*)', admin.site.root),
)

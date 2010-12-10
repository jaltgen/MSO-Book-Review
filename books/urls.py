# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('books.books.views',
    (r'^$', 'render_view', {'template_name':'index.html', 'data':{}}),
    (r'^list/$', 'book_list'),
    (r'^users/list/$', 'user_list'),

    (r'^ajax/book_list/$', 'ajax_book_list'),
    (r'^ajax/comment/add/$', 'ajax_comment_add'),
    (r'^view/(?P<b_id>\d*)/$', 'book_view'),
    (r'^bewertung/add/$', 'bewertung_add'),
    (r'^bewertung/edit/(?P<b_id>\d)/$', 'bewertung_add'),
    (r'^ajax/(?P<file>[\d\w]*\.[\d\w]{1,4})/$', 'ajax_handler'),
    (r'^error/$', 'error'),

    # Login Urls
    (r'^login/$', 'login_user'),
    (r'^logout/$', 'logout_user'),
)

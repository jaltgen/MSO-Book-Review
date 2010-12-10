# -*- coding: utf-8 -*-
"""   views.py

author: Jannik Altgen
contact: jannik.altgen@googlemail.com
since: 2009/08/09
summary: This python moduls contains the views for the books app, which is used to present reviews and so on.

"""

from models import *
from forms import *
import calendar
from datetime import datetime
from subroutines import *
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Min, Count
from django.conf import settings

def redirect_to_index(request):
    return HttpResponseRedirect(reverse("books.views.render_view"))

def render_view(request, template_name, data):
    """ Helper Function that fascilitates user authentication and group access """
    data['newest'] = Bewertung.objects.filter(is_rezension=True).order_by('-datum')[:5]
    data['root_path'] = settings.ROOT_PATH
    if request.user.is_authenticated():
        data['own_bewertung'] = Bewertung.objects.filter(benutzer=request.user, is_rezension=True)
        if len(data['own_bewertung']) == 0:
                    data['own_bewertung'] = False
    t = loader.get_template(template_name)
    rc = RequestContext(request, data)
    return HttpResponse(t.render(rc))


def login_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password','')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_view(request, 'users/login.html', {'success':True})

        else:
            return render_view(request, 'users/login.html', {'failure':True})
    else:
            return render_view(request, 'users/login.html', {'failure':True})

@login_required
def logout_user(request):
    logout(request)
    return render_view(request, 'users/logout.html', {})

def book_list(request, filter_args=None):
    """ View c"""

    return render_view(request, 'books/book_list.html', {})

def book_view(request, b_id):
    book = get_object_or_404(Buch, pk=b_id)
    reviews = Bewertung.objects.filter(buch=b_id, is_rezension=True)
    comments = Bewertung.objects.filter(buch=b_id, is_rezension=False)
    form = KommentarForm()
    return render_view(request, 'books/book_view.html', {'book':book,
                                                         'comments':comments,
                                                         'reviews':reviews,
                                                         'form':form})

@login_required
def bewertung_add(request, b_id=None):
    if b_id != None:
        bewertung_instance = get_object_or_404(Bewertung, pk=b_id)
        form = BewertungForm(instance=bewertung_instance)
    elif request.method == 'POST' and b_id == None: # If the form has been submitted...
        form_data = request.POST.copy()
        autor, created = Autor.objects.get_or_create(name=form_data['autor'])
        verlag, created = Verlag.objects.get_or_create(title=form_data['verlag'])
        form_data['autor'] = autor.pk
        form_data['verlag'] = verlag.pk
        form = BewertungForm(form_data, request.FILES) # A form bound to the POST data

        if form.is_valid():
            #Save image file
            try:
                filename = handle_uploaded_file(request.FILES['cover'])
            except:
                filename = ''

            # Genre object is instanciated from the form input genre
            genre = form.cleaned_data['genre']

            #Tag objects are created from the tag list, cleaned of whitespaces
            tag_list = form.cleaned_data['tags'].split(',')
            clean_tag_list = []
            for item in tag_list:
                new_tag = item.strip()
                new_tags = Tags(title=new_tag)
                new_tags.save()
                clean_tag_list += [new_tags.pk]

            user = request.user

            # Book object is created
            #if not Buch.objects.filter(title=form.cleaned_data['title']).count():
            #    message = "Ein Buch mit diesem Titel existiert bereits."
            #    return render_view(request, "errors/generic_error.html", {'message':message})

            new_buch = Buch(title=form.cleaned_data['title'],
                autor=autor,
                erscheinungsjahr=form.cleaned_data['erscheinungsjahr'],
                verlag=verlag,
                genre=genre,
                standort=form.cleaned_data['standort'],
                cover=filename)
            new_buch.save()

            # Tags are related to Buch
            for item in clean_tag_list:
                tag = get_object_or_404(Tags, pk=item)
                new_buch.tags.add(tag)

            #Bewertung is created and linked to the new Buch
            new_bewertung = Bewertung(schlagsatz=form.cleaned_data['bewertung_title'],
                                                                rating=form.cleaned_data['bewertung_rating'],
                                                                short=form.cleaned_data['bewertung_short'],
                                                                kommentar=form.cleaned_data['bewertung_rezension'],
                                                                buch=new_buch,
                                                                benutzer=user,
                                                                is_rezension=True)
            new_bewertung.save()

            return HttpResponseRedirect('/books/list/') # Redirect after POST
        else:
            form = BewertungForm(request.POST)
    else:
        form = BewertungForm()

    genre = Genre.objects.all()
    return render_view(request, 'forms/bewertung_add.html', {'form':form,
                                                             'all_autors':Autor.objects.all(),
                                                             'all_verlags':Verlag.objects.all()})

@login_required
def ajax_handler(request, file):
    loader = 'ajax/%s' % (file)
    return render_view(request, loader, {})

def ajax_book_list(request):
    item = request.GET['item']
    books = Buch.objects.all().order_by(item) # Normalfall
    if item == 'rating' or item == '-rating':
        books = Buch.objects.annotate(rating_average=Avg('bewertung__rating')).order_by('rating_average')
        if item == '-rating':
            books = Buch.objects.annotate(rating_average=Avg('bewertung__rating')).order_by('-rating_average')
    book_data = []
    for item in books:
        temp = {'object':item,
                'review_count':Bewertung.objects.filter(buch=item).count(),
                'rating':Bewertung.objects.filter(buch=item).aggregate(Avg('rating'))
                }
        book_data += [temp]
    return render_view(request, 'ajax/book_list_display.html', {'data':book_data})

@login_required
def ajax_comment_add(request):
    form = KommentarForm(request.POST)
    if form.is_valid():
        buch = get_object_or_404(Buch, pk=form.cleaned_data['kommentar_buch'])
        new_bewertung = Bewertung(schlagsatz=form.cleaned_data['kommentar_title'],
                                  rating=form.cleaned_data['kommentar_rating'],
                                  short='',
                                  kommentar=form.cleaned_data['kommentar_rezension'],
                                  buch=buch,
                                  benutzer=request.user,
                                  is_rezension=False)
        new_bewertung.save()
        return book_view(request, form.cleaned_data['kommentar_buch'])
    else:
        return error(request)

@login_required
def user_list(request):
    users_by_username = User.objects.all().annotate(bewertung_count=Count('bewertung')).order_by('username')
    users_by_rating = User.objects.annotate(bewertung_count=Count('bewertung')).order_by('-bewertung_count')
    user_name_list = []
    for item in users_by_username:
	temporary = {'username':item,
                     'buecher': Buch.objects.filter(bewertung__benutzer=item, bewertung__is_rezension = True)}
        user_name_list += [temporary]
    user_rating_list = []
    temporary = []
    for item in users_by_rating:
	temporary = {'username':item,
                     'buecher':Buch.objects.filter(bewertung__benutzer=item, bewertung__is_rezension=True)}
	user_rating_list += [temporary]
    return render_view(request, 'users/user_list.html', {'users_by_rating':user_rating_list,
                                                                                                           'users_by_username': user_name_list})

@login_required
def error(request):
    return render_view(request, "errors/generic_error.html", {})

# -*- coding: utf-8 -*-
"""   forms.py

author: Jannik Altgen
contact: jannik.altgen@googlemail.com
since: 2009/08/09
summary: This python moduls contains the forms for the books app, which represent the data input and provides validation (see Django Doc).

"""
from django import forms
from django.forms import ModelForm
from models import *

class BewertungForm(forms.Form):
    """ Form that represents the input for a new Bewertung including a new book and optional author/verlag adding functionality.
    This function corresponds to the workflow: a member always creates a book and writes a review for it. Thus, the user will have
    to create the book as well as assign or create an author and verlag. Books are checked for duplicates and if possible matches
    are found, a list of options will provided along with an error. """
    # Buch values
    title = forms.CharField(max_length=50)
    autor = forms.CharField(max_length=50) # Author option for regular form input
    erscheinungsjahr = forms.IntegerField()
    genre = forms.ModelChoiceField(Genre.objects.all())
    tags = forms.CharField()
    verlag = forms.CharField(max_length=50)
    standort = forms.CharField(max_length=25)
    cover = forms.ImageField(required=False)

    author_vorname = forms.CharField(required=False) # Author optional input if author does not exist, is checked in view
    author_nachname = forms.CharField(required=False)
    verlag_name = forms.CharField(required=False) # Verlag optional input in case verlag does not exist

    # Bewertung values
    bewertung_title = forms.CharField(max_length=50)
    bewertung_rating = forms.IntegerField(min_value=1, max_value=5)
    bewertung_short = forms.CharField(widget=forms.Textarea)
    bewertung_rezension = forms.CharField(widget=forms.Textarea)

class KommentarForm(forms.Form):
    """ Form which represents the input from users in the book view, which represents the Commnts on books, also including the Ratings and so ons """
    kommentar_title = forms.CharField()
    kommentar_rating = forms.IntegerField(min_value=1, max_value=5)
    kommentar_rezension = forms.CharField(widget = forms.Textarea)
    kommentar_buch = forms.IntegerField()

# -*- coding: utf-8 -*-
"""   models.py

author: Jannik Altgen
contact: jannik.altgen@googlemail.com
since: 2009/08/09
summary: Diese models.py enthaelt die DB Modelle für den MSO Bookstore

"""

from django.db import models
from django.contrib.auth.models import User

class Verlag(models.Model):
    """ Datenbank Model für Verlage, welche separat mit Büchern verlinkt sind, aber nur einmalig in der Datenbank auftauchen"""
    title = models.CharField(max_length=50)

    def __unicode__(self):
        """ Unicode Funktion für Default Output"""
        return unicode(self.title)

class Tags(models.Model):
    """ Datenbank Model welches die möglichen Tags für Bücher repräsentiert"""
    title = models.CharField(max_length=15)

    def __unicode__(self):
        """ Unicode Funktion für Default Output"""
        return unicode(self.title)

class Genre(models.Model):
    """ Datenbankmodel welches die verschiedenen Genres anzeigt"""
    title = models.CharField(max_length=50)
    beschreibung = models.TextField()

    def __unicode__(self):
        """ Unicode Funktion für Default Output"""
        return str(self.title)

class Autor(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

class Buch(models.Model):
    """ DB Model für ein Buch. Diese Klasse wird für jedes Werk einmalig instanziert um dann verschiedene Bewertungen erhalten zu können"""
    title = models.CharField(max_length=50)
    erscheinungsjahr = models.IntegerField()
    standort = models.CharField(max_length=50)
    tags = models.ManyToManyField(Tags)
    verlag = models.ForeignKey(Verlag)
    autor = models.ForeignKey(Autor)
    genre = models.ForeignKey(Genre)
    cover = models.CharField(max_length=50)
    datum = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        """ Unicode Funktion für Default Output"""
        return unicode(self.title)

class Bewertung(models.Model):
    """ Generische Klasse für Bewertungen für Bücher, somit können mehrere Bewertungen für einzelne Bücher eingetragen werden."""
    benutzer = models.ForeignKey(User)
    rating = models.IntegerField()
    kommentar = models.TextField()
    schlagsatz = models.TextField()
    datum = models.DateTimeField(auto_now_add=True)
    buch = models.ForeignKey(Buch)
    short = models.TextField()
    is_rezension = models.BooleanField()
    def __unicode__(self):
        """ Unicode Funktion für Default Output"""
        return_string = "%s, %s , %s" % (self.schlagsatz, self.datum, self.benutzer)
        return unicode(return_string)

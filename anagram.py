import webapp2;
import os;
import jinja2;
import random;
from google.appengine.ext import ndb;
from google.appengine.api import users
from myuser import MyUser

class Anagram(ndb.Model):
    AnagramKey = ndb.StringProperty()
    User = ndb.StringProperty()
    # Anagram = ndb.StringProperty()
    WordList = ndb.StringProperty(repeated = True)
    WordCount = ndb.IntegerProperty()
    LetterCount = ndb.IntegerProperty()

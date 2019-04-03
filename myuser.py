from google.appengine.ext import ndb
class MyUser(ndb.Model):
    username = ndb.StringProperty()
    myAnagram = ndb.IntegerProperty()
    myWordCount = ndb.IntegerProperty()

import webapp2;
import os;
import jinja2;
import random;
from google.appengine.ext import ndb;
from google.appengine.api import users
from myuser import MyUser
from anagram import Anagram
import re
from itertools import  combinations

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

def lexi(word):
    list1 = list(word.lower())
    sorted_list = sorted(list1)
    return ''.join(sorted_list)

def subSort(word):
    listWord = list(word)
    word_keys = []
    for i in range(3,len(word)+1):
        temp=(["".join(c)for c in combinations(word,i)])
        for c in temp:
            word_keys.append(c)
    return word_keys

class SubAnagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        message = "Welcome to sub anagram search page"
        resultList =[]
        template_values = {
        'message':message,
        'subAna':resultList
        }
        template = JINJA_ENVIRONMENT.get_template('subanagram.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser',user.user_id())
        myuser = myuser_key.get()

        resultList =[]

        action = self.request.get('button')
        if action == 'SEARCH':
            word = self.request.get('word')

            if word=="":
                self.redirect('/subanagram')
            else:
                lexi_word = lexi(word)

                subList = subSort(lexi_word)
                for key in subList:
                    word_key = ndb.Key('Anagram',user.email()+key)
                    word = word_key.get()

                    if word == None:
                        continue
                    else:
                        resultList.extend(word.WordList)
                template_values = {
                'subAna':resultList,
                'message':"Displaying sub anagrams"
                }
                template = JINJA_ENVIRONMENT.get_template('subanagram.html')
                self.response.write(template.render(template_values))
        else:
            self.redirect('/subanagram')

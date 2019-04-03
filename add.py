import webapp2;
import os;
import jinja2;
import random;
from google.appengine.ext import ndb;
from google.appengine.api import users
from myuser import MyUser
from anagram import Anagram
import re

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

class Add(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        Message = "Welcome to Anagram addition page"
        template_values ={
        'message':Message
        }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        user = users.get_current_user()


        user_key =ndb.Key('MyUser',user.user_id())
        user_info = user_key.get()


        def lexi(word):
            list1 = list(word.lower())
            sorted_list = sorted(list1)
            # print(sorted_list)
            return ''.join(sorted_list)

        if action=='Add':
            original_word = (self.request.get('Word')).lower()

            if not re.match("^[a-z]*$", original_word.lower()):
                message = "Please enter alphabets only"

            else:

                Word = lexi(self.request.get('Word'))
                anagram_key = ndb.Key('Anagram',user.email()+Word)
                anagram = anagram_key.get()
                # & anagram.User != user
                if anagram == None :
                    new_anagram = Anagram(id=user.email()+Word,AnagramKey=Word)
                    new_anagram.User=user.email()
                    new_anagram.WordList.append(original_word)
                    new_anagram.WordCount = 1
                    new_anagram.LetterCount =  len(original_word)
                    new_anagram.put()

                    user_info.myAnagram = user_info.myAnagram + 1
                    user_info.myWordCount = user_info.myWordCount + 1
                    user_info.put()

                    message = "Word added"

                else:
                    flag = False
                    for word in anagram.WordList:
                        if word == original_word:
                            flag = True
                            break
                        else:
                            flag = False

                    if flag:
                        message = "Word already exists"
                    else:
                        # anagram.User=user.email()
                        anagram.WordList.append(original_word)
                        anagram.WordCount = anagram.WordCount + 1
                        anagram.put()
                        message = "Word added"


                        user_info.myWordCount = user_info.myWordCount + 1
                        user_info.put()


            template_values ={
            'message':message
            }
            template = JINJA_ENVIRONMENT.get_template('add.html')
            self.response.write(template.render(template_values))

            # self.redirect('/')

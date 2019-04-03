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

class Upload(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        message = "Welcome to file upload page"
        template_values = {
        'message':message
        }
        template = JINJA_ENVIRONMENT.get_template('upload.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        file = self.request.get('myFile')

        def lexi(word):
            list1 = list(word.lower())
            sorted_list = sorted(list1)
            return ''.join(sorted_list)

        if action == 'UPLOAD':

            f = open(file)
            line = f.readline()
            # count = 1
            while line:
                original_word = (line.strip('\n\r')).lower()
                lexi_word = lexi(original_word)

                anagram_key = ndb.Key('Anagram',user.email()+lexi_word)
                anagram = anagram_key.get()
                if anagram == None:
                    new_anagram = Anagram(id=user.email()+lexi_word,AnagramKey=lexi_word)
                    new_anagram.User=user.email()
                    new_anagram.WordList.append(original_word)
                    new_anagram.WordCount = 1
                    new_anagram.LetterCount =  len(original_word)
                    new_anagram.put()

                    myuser.myAnagram = myuser.myAnagram + 1
                    myuser.myWordCount = myuser.myWordCount + 1
                    myuser.put()
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
                        # message = "Word added"


                        myuser.myWordCount = myuser.myWordCount + 1
                        myuser.put()

                # count = count + 1
                line = f.readline()

            f.close()

        template_values={
                'message':"File Uploaded"
                }
        template = JINJA_ENVIRONMENT.get_template('upload.html')
        self.response.write(template.render(template_values))

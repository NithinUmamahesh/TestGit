import webapp2;
import os;
import jinja2;
import random;
from google.appengine.ext import ndb;
from google.appengine.api import users
from myuser import MyUser
from add import Add
from anagram import Anagram
from upload import Upload

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user == None:
            template_values = {
            'login_url' : users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
            self.response.write(template.render(template_values))
            return
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(username=user.email(),id=user.user_id(),myAnagram=0,myWordCount=0)
            myuser.put()
        ana = Anagram.query().fetch()
        # c = Counter();
        template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'user':user,
            'myuser':myuser,
            'ana':ana
            # ,
            # 'counter': getAnaCount()
            }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'SEARCH':

            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            def lexi(word):
                list1 = list(word.lower())
                sorted_list = sorted(list1)
                return ''.join(sorted_list)

            searchText = (self.request.get('word')).lower()
            if searchText == "":
                message = "Word not found"
                template_values={
                    'user':user,
                    'message': "Word not found",
                    'ana': Anagram.query().fetch()
                    }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))
            else:
                search_key = lexi(searchText)

                ana_key = ndb.Key("Anagram",user.email()+search_key)
                ana = ana_key.get()
                # message = " Word found"

            # ana1 = Anagram.query();
            # ana =ana1.filter(Anagram.AnagramKey == search_key).fetch(keys_only = True)

                template_values={
                    'ana':ana,
                    'user':user,
                    'myuser':myuser
                    }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))




app = webapp2.WSGIApplication([('/',MainPage),('/add',Add),('/upload',Upload)],debug = True)

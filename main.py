import webapp2
import urllib2
import urllib
import json
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb

#Icons designed by Gregor Cresnar from Flaticon


jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class people(ndb.Model):
	name = ndb.StringProperty()
	number = ndb.IntegerProperty()
	email = ndb.StringProperty()

class text(ndb.Model):
	feed = ndb.StringProperty()
	reciever = ndb.StringProperty()
	

class MainHandler(webapp2.RequestHandler):
	def get(self):

		template = jinja_environment.get_template('main.html')
		self.response.write(template.render())
		 

	def post(self):
		feed_from_form = self.request.get('Message')
		
		feed_model = text(feed=feed_from_form)
		feed_model.put()

		template = jinja_environment.get_template('main_out.html')
		self.response.write(template.render(
			{
				'text': feed_from_form 
			}
			))

class ContactsHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('contacts.html')
		self.response.write(template.render())

	def post(self):
		name_from_form = self.request.get('Contact_name')



class ManageHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('manage.html')
		self.response.write(template.render())

class HelpHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('help.html')
		self.response.write(template.render())

class SettingHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('settings.html')
		self.response.write(template.render())

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		
		user = users.get_current_user()
		if user:
			nickname = user.nickname()
			logout_url = users.create_logout_url('/')
			greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(nickname, logout_url)
		else:
			login_url = users.create_login_url('/')
			greeting = '<a href="{}">Sign in</a>'.format(login_url)

		self.response.write('<html><body>{}</body></html>'.format(greeting))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/contacts', ContactsHandler),
    ('/help', HelpHandler),
    ('/settings', SettingHandler),
    ('/manage', ManageHandler),
    ('/login', LoginHandler),
], debug=True)

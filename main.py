import webapp2
import urllib2
import urllib
import json
import jinja2
import os
import logging

from google.appengine.api import users
from google.appengine.ext import ndb

#Icons designed by Gregor Cresnar from Flaticon


jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class OurUser(ndb.Model):
	user = ndb.StringProperty()
	username = ndb.StringProperty()
	

class People(ndb.Model):
	name = ndb.StringProperty()
	number = ndb.IntegerProperty()
	email = ndb.StringProperty()
	##username = user
	
class Text(ndb.Model):
	feed = ndb.StringProperty()
	receiver = ndb.StringProperty()
	user = ndb.StringProperty()
	timestamp = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		user_list = OurUser.query(OurUser.user == user.user_id()).fetch()
		logging.info(user_list)
		
		if len(user_list) == 0:
			self.redirect("/username")

		template = jinja_environment.get_template('main.html')
		self.response.write(template.render())

		 

	def post(self):
		feed_from_form = self.request.get('Message')
		receiver_from_form = self.request.get('recpient')
		user = users.get_current_user()
		

		
		feed_model = Text(feed=feed_from_form, receiver=receiver_from_form, user=user.email())
		feed_model.put()
		

		template = jinja_environment.get_template('main_out.html')
		self.response.write(template.render(
			{
				'feed': feed_from_form,
				'receiver': receiver_from_form,
				'user': user
				 
			}
			))

class UsernameHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('username.html')
		self.response.write(template.render())

	def post(self):
		user = users.get_current_user()

		u_id = user.user_id()
		username = self.request.get('username')

		ouruser_model = OurUser(user = u_id, username = username)
		ouruser_model.put()

		self.redirect("/")




class ContactsHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('contacts.html')
		self.response.write(template.render())

	def post(self):
		username_from_form = self.request.get('contact_name')
		email_from_form = self.request.get('contact_email')
		phone_number_from_form = self.request.get('contact_number')

		phone_number_from_form = int(phone_number_from_form)

		contact_model = People(name = username_from_form, email = email_from_form, number= phone_number_from_form)
		contact_model.put()

		template = jinja_environment.get_template('contacts_out.html')
		self.response.write(template.render(
			{
				'contact': contact_model
			}))



class ManageHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		user_email = user.email()
		list_of_messages = Text.query(Text.receiver == user_email).order(-Text.timestamp).fetch()

		template = jinja_environment.get_template('manage.html')
		self.response.write(template.render({
			'Text': list_of_messages
			}
			))
			

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
    ('/username', UsernameHandler)
], debug=True)

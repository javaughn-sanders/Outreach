import webapp2
import urllib2
import urllib
import json
import jinja2
import os

from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('main.html')
		self.response.write(template.render()) 





class ContactsHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('contacts.html')
		self.response.write(template.render())

class ManageHandler(webapp2.RequestHandler):
	def get(template):
		template = jinja_environment.get_template('manage.html')
		self.response.write(template.render())

class HelpHandler(webapp2.RequestHandler):
	def get(template):
		template = jinja_environment.get_template('help.html')
		self.response.write(template.render())

class SettingHandler(webapp2.RequestHandler):
	def get(template):
		template = jinja_environment.get_template('settings.html')
		self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/contacts', ContactsHandler),
    ('/help', HelpHandler),
    ('/settings', SettingHandler),
    ('/manage', ManageHandler),
], debug=True)

import webapp2
import urllib2
import urllib
import json
import jinja2
import os

from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

##class TextBox(ndb.Model):
	##Txtbox = 

class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('main.html')
		self.response.write(template.render()) 

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

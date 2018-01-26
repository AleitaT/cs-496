#########################################################
# Author: Aleita Train
# OSU ONLINE CS 496
# WINTER 2018
#

from google.appengine.ext import ndb
import webapp2
import json

from models import Boat, BoatHandler, Slip, SlipHandler

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Hello, World!')
    from datetime import datetime
    self.response.write(str(datetime.now()))


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boat', BoatHandler),
    ('/boat/(.*)', SlipHandler),
    ('/slip', BoatHandler),
    ('/slip/(.*)', SlipHandler),
], debug=True)

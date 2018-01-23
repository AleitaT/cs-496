from google.appengine.ext import ndb
import webapp2
import json

class Fish(ndb.Model):
    name = ndb.StringProperty(required=True)
    ph_min = ndb.IntegerProperty()
    ph_max = ndb.IntegerProperty()

class FishHandler(webapp2.RequestHandler):
    def post(self):
        # sending in data and savin to json object 
        fish_data = json.loads(self.request.body)
        # for making a new fish
        new_fish = Fish(name=fish_data['name'])
        new_fish.put()
        fish_dict = new_fish.to_dict()
        fish_dict['self'] = '/fish/' + new_fish.key.urlsafe()
        # dumping this data back out
        self.response.write(json.dumps(fish_dict))        
    def get(self, id=None):
        # if an id exists
        if id: 
            # f now holds our fish 
            f = ndb.Key(urlsafe=id).get()
            f_d = f.to_dict()
            f_d['self'] = "/fish/" + id
            self.response.write(json.dumps(f_d))
        
class Boat(ndb.Model):
    id = ndb.KeyProperty(required=True)
    name = ndb.StringProperty
    type = ndb.StringProperty
    length = ndb.IntegerProperty
    at_sea = ndb.BooleanProperty

class BoatHandler(webapp2.RequestHandler):
    def post(self):

    def get(self, id=None):

class Slip(ndb.Model):
    id = ndb.KeyProperty(required=True)
    number = ndb.IntegerProperty
    current_boat = ndb.StringProperty
    arrival_date = ndb.DateProperty
    departure_history = ndb.StringProperty(repeat=True) 


class SlipHandler(webapp2.RequestHandler):



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
    ('/fish', FishHandler),
    ('/fish/(.*)', FishHandler)
], debug=True)

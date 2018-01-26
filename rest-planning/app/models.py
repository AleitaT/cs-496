###########################################################
# Author: Aleita Train
# REST PLANNING 
# OSU ONLINE CS 496 
# Winter 2018 
# Uses google app engine and webapp2 to serve a restful api
#############################################################

from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
  name = ndb.StringProperty()
  type = ndb.StringProperty()
  length = ndb.IntegerProperty()
  at_sea = ndb.BooleanProperty()

class BoatHandler(webapp2.RequestHandler):
  def post(self):
    # all boards should start at sea
    body['at_sea'] = True
    boat_data = json.loads(self.request.body)
    new_boat = Boat(name=boat_data['name'])
    new_boat.put()
    boat_dict = new_boat.to_dict()
    boat_dict['self'] = '/boat/' + new_board.key.urlsafe()
    self.response.write(json.dumps(boat_dict))
  def delete(self):
    # deleting a ship should empty the slip the boat was in
  def patch(self):
     # if modify to make at sea remove the boat from the other slip
     # setting ship to be at sea and updating slip status should
     # happen under one same api call
     # if updating slip number error if slip is taken 403
     # return the slip, date of arrival and boat
    if id:
      boat = ndb.Key(urlsafe=id).get()
      if boat:
        b_d = json.loads(self.request.body)
        if 'name' in boat_data:
          boat.name = boat_data['name']
        if 'type' in boat_data
          boat.type = boat_data['type']
        if 'length' in boat_data
          boat.length = boat_data['length']
        if 'at_sea' in boat_data
          boat.at_sea = boat_data['at_sea']
        boat.put()
        boat_dict = boat.to_dict()
        self.response.write(jsonDumps(boat_dict))

  def get(self, id=None):
    if id:
      b = ndb.Key(urlsafe=id).get()
      b_d = b.to_dict()
      b_d['self'] = "/boat/" + id
      self.response.write(json.dumps(b_d))
    else: 
        #if no id is provided display entire list of boats
        boats = Boat.query().fetch()
        boat_dicts = {'Boats':[]}
        for boat in boats:
          id = boat.key.urlsafe()
          b_d = boat.to_dict()
          b_d['self'] = '/boats/' + id
          b_d['id'] = id
          b_d['Boats'].append(boat_data)
    def delete(self, id=None)
      if id:
        boat = ndb.Key(urlsafe=id).get()
        boat.key.delete()
        self.response.write('Boat has been delete')
      else: 
        self.response.status = 'Error 405 Bad ID'
        self.response.write("Error: bad id provided")

    
 
class Slip(ndb.Model):
  id = ndb.KeyProperty(required=True)
  number = ndb.IntegerProperty()
  current_boat = ndb.StringProperty()
  arrival_date = ndb.DateProperty()
  # departure_history = ndb.StringProperty(repeat=True) 

class SlipHandler(webapp2.RequestHandler):
  def post(self):
    slip_data = json.loads(self.request.body)
    new_slip = Slip(name=slip_data['name'])
    new_slip.put()
    slip_dict = new_slip.to_dict()
    slip_dict['self'] = "/slip/" + new_slip.key.urlsafe()
    self.response.write(json.dumps(slip_dict))
  def get(seld, id=None):
    if id:
      s = ndb.Key(urlsafe=id).get()
      s_d = s.to_dict()
      s_d['self'] = "/slip" + id
      self.response.write(json.dumps(b_d))
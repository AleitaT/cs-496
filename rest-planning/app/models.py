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
from format import jsonHandler, getAPIObject


class Boat(ndb.Model):
  name = ndb.StringProperty(required=True)
  type = ndb.StringProperty(required=True)
  length = ndb.IntegerProperty(required=True)
  at_sea = ndb.BooleanProperty()

class BoatHandler(webapp2.RequestHandler):

  def __init__(self, *args, **kwargs):
    self.err = False
    super(BoatHandler, self).__init__(*args, **kwargs)

  def _sendErr(self, code, message):
    self.response.status = code
    self.response.write(message)
    self.err = True

  # tested and works returns json format with key id 
  def post(self, request):    
    try:
      body = json.loads(self.request.body)
    except ValueError:
      self._sendErr(405, "Error: Body is not required JSON format.")

    if not self.err:
      # all boats should start at sea
      body['at_sea'] = True
      new_boat = Boat(**body)
      new_boat.put()
      boat_dict = new_boat.to_dict()
      boat_dict['id'] = new_boat.key.urlsafe()
      boat_dict['self'] = '/boats/' + new_boat.key.urlsafe()
      self.response.write(jsonHandler(boat_dict))
 
  # tested and updates successfully
  def patch(self, id=None):
    if id:
      boat = ndb.Key(urlsafe=id).get()
      if boat:
        boat_data = json.loads(self.request.body)
        if 'name' in boat_data:
          boat.name = boat_data['name']
        if 'type' in boat_data:
          boat.type = boat_data['type']
        if 'length' in boat_data:
          boat.length = boat_data['length']
        if 'at_sea' in boat_data:
          boat.at_sea = boat_data['at_sea']
        boat.put()
        boat_dict = boat.to_dict()
        self.response.write(jsonHandler(boat_dict))
      else:
        self.response.status = "405 Bad ID";
        self.response.write("Error: Bad ID provided")
    else:
      self.response.status = "403 Bad Id";
      self.response.write("Error: Id required for PATCH")

  # tested and working, returns arrat o boat items in boats
  def get(self, id=None):
    if id:
      boat = ndb.Key(urlsafe=id).get()
      if boat:
        boat_dict= boat.to_dict()
        boat_dict['self'] = "/boats/" + id
        self.response.write(jsonHandler(boat_dict))
      else:
        self._sendErr(405, "Error: lacking boat ID")
    else: 
        #if no id is provided display entire list of boats
        boats = Boat.query().fetch()
        boat_dicts = {'Boats':[]}
        for boat in boats:
          id = boat.key.urlsafe()
          boat_data = boat.to_dict()
          boat_data['self'] = '/boats/' + id
          boat_data['id'] = id
          boat_dicts['Boats'].append(boat_data)

        self.response.write(jsonHandler(boat_dicts))
  #testing
  def delete(self, id=None):
    if id:
      boat = ndb.Key(urlsafe=id).get()
      if boat:
        for slip in Slip.query(Slip.current_boat == id):
          if slip.current_boat and slip.arrival_date:
            slip.current_boat = ""
            slip.arrival_date = ""
            slip.put()
        boat.key.delete()
        self.response.write('Boat has been deleted')
      else:
        self.response.status = 'Error 405 Bad ID';
        self.response.write("Error: bad id provided")
    else: 
      self.response.status = "403 No Id";
      self.response.write("Error: Id required for DELETE")

  def put(self, id=None):
    if id: 
      put_data = json.loads(self.request.body)
      put_boat = ndb.Key(urlsafe=id).get()
      if 'name' in put_data:
        if 'type' in put_data: 
          if 'length' in put_data:
            put_boat.name = put_data['name']
            put_boat.type = put_data['type']
            put_boat.length = put_data['length']
            put_boat.put()
            self.response.write("we did it")
          else: 
            self.response.write("we need length, type, and name")
        else: 
          self.response.write("we need length, type, and name")
      else: 
        self.response.write("we need length, type, and name")

##############################################################
#
#                       SLIP MODEL
#
##############################################################
class Slip(ndb.Model):
  number = ndb.IntegerProperty(required=True)
  current_boat = ndb.StringProperty()
  arrival_date = ndb.StringProperty()
  # departure_history = ndb.StringProperty(repeat=True) 

  def prepareSlip(self):
    id = self.key.urlsafe()
    slip_data = self.to_dict()
    slip_data['id'] = id
    slip_data['self'] = '/slips/' + id
    if slip_data['current_boat'] != 'null':
      slip_data['boat_link'] = '/boats/' + slip_data['current_boat']
    return jsonHandler(slip_data)

##############################################################
#
#                       SLIP ROUTE
#
##############################################################
class SlipHandler(webapp2.RequestHandler):

  def __init__(self, *args, **kwargs):
    self.err = False
    super(SlipHandler, self).__init__(*args, **kwargs)

  def _sendErr(self, code, message): 
    self.response.status = code
    self.response.write(message)
    self.err = True    

  def post(self, id=None):    
    try:
      body = json.loads(self.request.body)
    except:
      self._sendErr(405, "Error: Body is not required JSON format.")
    if Slip.query(Slip.number == body['number']).get(): 
      self._sendErr(403, "Error: A slip of that numer already exists.")
    if not self.err:
      body['current_boat'] = "null";
      # all boards should start at sea
      new_slip = Slip(**body)
      new_slip.put()
      self.response.write(new_slip.prepareSlip())

  def get(self, id=None):
    if id:
      slip = ndb.Key(urlsafe=id).get()
      if slip:
        slip_dict = slip.to_dict()
        slip_dict['self'] = "/slips/" + id
        self.response.write(jsonHandler(slip_dict))
      else:
        self._sendErr(405, "Error: lacking slip ID")
    else: 
        #if no id is provided display entire list of boats
        slips = Slip.query().fetch()
        slip_dicts = {'Slips':[]}
        for slip in slips:
          id = slip.key.urlsafe()
          slip_data = slip.to_dict()
          slip_data['self'] = '/slips/' + id
          slip_data['id'] = id
          slip_dicts['Slips'].append(slip_data)

        self.response.write(jsonHandler(slip_dicts))

  def delete(self, id=None):
    if id:
      slip = ndb.Key(urlsafe=id).get()
      if slip:
        slip.key.delete()
        self.response.write('Slip has been deleted')
      else:
        self.response.status = 'Error 405 Bad ID'
        self.response.write("Error: bad id provided")
    else: 
      self.response.status = "403 No Id";
      self.response.write("Error: Id required for delete call")

  def patch(self, id=None):
    if id:
      slip = ndb.Key(urlsafe=id).get()
      if slip:
        slip_data = simplejson.loads(self.request.body)
        if 'number' in slip_data:
          if Slip.query(Slip.number == slip_data['number']).get(): 
            self._sendErr(403, "Error: A slip of that numer already exists.")
          slip.number = slip_data['number']
        slip.put()
        slip_dict = slip.to_dict()
        self.response.write(jsonHandler(slip_dict))
      else:
        self.response.status = "405 Bad ID";
        self.response.write("Error: Bad ID provided")
    else:
      self.response.status = "403 Bad Id";
      self.response.write("Error: Id required for PATCH")

##############################################################
#
#                  BOAT ARRIVAL HANDLER ROUTE
#
##############################################################
class BoatArrivalHandler(webapp2.RequestHandler):
  def _sendErr(self, code, message):
      self.response.status = code
      self.response.write(message)
      self.err=True

  def put(self, slip_id):
    self.err = False
    print(self.request.body)
    err = False
    try: 
      body = json.loads(self.request.body)
    except ValueError: 
      self._sendErr(405, "Json error")
    if not self.err:
      boat = getAPIObject(body['boat_id'])
      print(boat)
      self.response.write(1)
      if not boat:
        self._sendErr(405, "Error this boat doesn't exist")
    if not self.err:
      slip = getAPIObject(slip_id)
      if not slip:
        self._sendErr(405, "Error this slip id is falsey")
    if not self.err:
      if slip.current_boat != 'null':
        self._sendErr(403, "Error: this slip is occupado")
    if not self.err:
      slip.arrival_date = body['arrival_date']
      slip.current_boat = body['boat_id']
      boat.at_sea = False
      boat.slip = slip_id
      slip.put()
      boat.put()


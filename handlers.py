from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

import logging
import os.path
import webapp2
import json

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from models import *
from BaseHandlers import *


'''
Function to serialize arbitrary objects to their json representation
'''
def json_object_serializer(obj):
  if hasattr(obj, 'isoformat'):
    return obj.isoformat()
  else:
    raise TypeError(('Object of type {0} with value of {1} is ' 'not JSON serializable').format(type(obj), repr(obj)))

def shifts_to_dict(shifts):
  result=[]
  for shift in shifts:
    user = shift.user.get().to_dict()
    vals = {}
    vals['datetime']=shift.datetime
    vals['sub']=shift.sub
    vals['duration']=shift.duration
    vals['status']=shift.status
    vals['user']=user
    result.append(vals)
  ans = {'shifts': result}
  return ans

class GetShiftsHandler(BaseHandler):
  '''
  Returns a shifts attribute with a list of all shifts in the database as a json object
  '''
  @user_required
  def get(self):
    s = Shift.query()
    result = shifts_to_dict(s)
    response=json.dumps(result, default=json_object_serializer)
    #self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    self.response.out.write(response)

class GetShiftsByUserHandler(BaseHandler):
  '''
  Return the shifts for the user passed in as parameter
  '''

  @user_required
  def get(self):
    user=self.user
    shifts = Shift.query(Shift.user == user.key)
    result = shifts_to_dict(shifts)
    response=json.dumps(result, default=json_object_serializer)
    self.response.out.write(response)







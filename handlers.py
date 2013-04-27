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

'''Write all the custom handlers here'''

def json_object_serializer(obj):
  if hasattr(obj, 'isoformat'):
    return obj.isoformat()
  else:
    raise TypeError(('Object of type {0} with value of {1} is ' 'not JSON serializable').format(type(obj), repr(obj)))

class GetShiftsHandler(BaseHandler):
  @user_required
  def get(self):
    s = Shift.query()
    # SEND BACK THE USER AS WELL. NOT THE OBJECT BUT INSTEAD THE ACTUAL VALUES OF THE PROPERTIES OF THE USER ASSOCIATED WITH EACH USER
    shifts = []
    for shift in s:
      vals = {}
      vals['datetime']=shift.datetime
      vals['sub']=shift.sub
      vals['duration']=shift.duration
      vals['status']=shift.status
      shifts.append(vals)
    result = {'shifts': shifts}
    response=json.dumps(result, default=json_object_serializer)
    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    self.response.out.write(response)
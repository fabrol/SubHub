from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

import logging
import os.path
import webapp2

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from models import *
from BaseHandlers import *

'''Write all the custom handlers here'''

class GetShiftsHandler(BaseHandler):
  @user_required
  def get(self):
    s = Shift.query()
    params = {'shifts':s}
    self.response.out.write(params)

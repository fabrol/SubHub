from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.api import mail

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
import datetime


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
    vals['sub']=shift.sub.get().to_dict()
    vals['duration']=shift.duration
    vals['status']=shift.status
    vals['user']=user
    result.append(vals)
  ans = {'shifts': result}
  return ans

class GetCurrentUser(BaseHandler):
  '''
  Returns the current user
  '''
  @user_required
  def get(self):
    user = self.user.to_dict()
    response = json.dumps(user,default=json_object_serializer)
    self.response.out.write(response)

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


class  RequestSubHandler(BaseHandler):
    '''
    Send email to users about new open shift. Email includes link for claiming/viewing
    '''
    
    @user_required
    def post(self):

        response = json.loads(self.request.body)
        user = self.user
        sender_address = "newshift@submyshift.appspotmail.com"
        subject = response['shift']['datetime'] 
        body = "here is a sample body"
    
        u = User.query()
        for recipient in u:
            if recipient.email_address is not user.email_address:
                print recipient.email_address
                mail.send_mail(sender_address, '<'+recipient.email_address+'>', subject,body) 
        ourdatetime = datetime.datetime.strptime(response['shift']['datetime'],'%Y-%m-%dT%H:%M:%S')
        print ourdatetime
        q = Shift.query()
        curShift = q.filter((Shift.datetime == ourdatetime)).fetch(1)
        curShift[0].status = "closed"
        curShift[0].put()

class ClaimSubHandler(BaseHandler):
    '''
    Handle claims for subbing shifts. E-mail the original user about the claim
    '''
    
    @user_required
    def post(self):
        sub = self.shift.sub
        user = self.user
        user_address = user.e-mail_address
        if not mail.is_emailvalid(user_address):
            print "hello"#email address not valid?
        else:
            sender_address = "claimedshift@submyshift.appspotmail.com"
            subject = sub.name + " has claimed your shift!"
            body = """ MESSAGE BODY YO """
            mail.send_mail(sender_address, user_address, subject, body)
        
      
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
from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2Decorator


CLIENT_ID="1030576108060.apps.googleusercontent.com"
CLIENT_SECRET="vOl0WwYYfDjEAml7_tNyN_2J"
SCOPE="https://www.googleapis.com/auth/calendar"

decorator = OAuth2Decorator(
		  client_id=CLIENT_ID,client_secret=CLIENT_SECRET,scope=SCOPE)


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
    vals['endtime']=shift.endtime
    if shift.sub:
      vals['sub']=shift.sub.get().to_dict()
    else:
      vals['sub']='NONE'
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


class RequestSubHandler(BaseHandler):
    '''
    Send email to users about new open shift. Email includes link for claiming/viewing
    '''
    
    @user_required
    def post(self):

        response = json.loads(self.request.body)
        user = self.user
        sender_address = "newshift@submyshift.appspotmail.com"
        subject = repr(response['shift']['datetime'])
        body = "here is a sample body"

        # ADD ENCRYPTION FOR SENDING INFO
    
        u = User.query()
        for recipient in u:
            if recipient.email_address is not user.email_address:
                viewlink = self.uri_for('authenticated',user_id=recipient.get_id(),_full=True)
                claim_url = self.uri_for('claim', user_email=recipient.email_address,
                date_time=response['shift']['datetime'], _full=True)
                print claim_url
                mybody = """A new shift has opened up!
                click here to view - %s 
                click here to claim - %s
                """ % (viewlink, claim_url)
                print mybody
                mail.send_mail(sender_address, '<'+recipient.email_address+'>', subject, mybody) 
        ourdatetime = datetime.datetime.strptime(response['shift']['datetime'],'%Y-%m-%dT%H:%M:%S')
        q = Shift.query()
        curShift = q.filter((Shift.datetime == ourdatetime)).fetch(1)
        curShift[0].status = "open"
        curShift[0].put()
        self.response.set_status(200)
        self.response.out.write(json.dumps('{success:true}'))

class RequestSubofSubHandler(BaseHandler):
    '''
    Send email to users about new open shift that was previously subbed. Email includes link for claiming/viewing
    '''
    
    @user_required
    def post(self):

        response = json.loads(self.request.body)
        #The current user is the one who has the sub
        cur_sub_user = self.user
        sender_address = "newshift@submyshift.appspotmail.com"
        subject = repr(response['shift']['datetime'])
        body = "here is a sample body"

        # ADD ENCRYPTION FOR SENDING INFO
    
        u = User.query()
        for recipient in u:
            if recipient.email_address is not cur_sub_user.email_address:
                viewlink = self.uri_for('authenticated',user_id=recipient.get_id(),_full=True)
                claim_url = self.uri_for('claim', user_email=recipient.email_address,
                date_time=response['shift']['datetime'], _full=True)
                print claim_url
                mybody = """A new shift has opened up!
                click here to view - %s 
                click here to claim - %s
                """ % (viewlink, claim_url)
                print mybody
                mail.send_mail(sender_address, '<'+recipient.email_address+'>', subject, mybody) 
        ourdatetime = datetime.datetime.strptime(response['shift']['datetime'],'%Y-%m-%dT%H:%M:%S')
        q = Shift.query()
        curShift = q.filter((Shift.datetime == ourdatetime)).fetch(1)
        curShift[0].status = "open"
        curShift[0].sub = None
        curShift[0].put()
        self.response.set_status(200)
        self.response.out.write(json.dumps('{success:true}'))


def UpdateSubForSelf(shift):
  if (shift.sub == shift.user):
    shift.sub = None
    shift.status = "normal"
    shift.put()
    return True
  else:
    return False

class ClaimSubEmailHandler(BaseHandler):
  '''
  Handles direct link from email to take sub
  '''
  def get(self):
    user = None
    user_email_address = self.request.get('user_email')
    shift_datetime = self.request.get('date_time')
    
    ourdatetime = datetime.datetime.strptime(shift_datetime,'%Y-%m-%dT%H:%M:%S')
    curShift = Shift.query().filter(Shift.datetime == ourdatetime).fetch(1)
    
    if curShift[0].status != 'open':
        print 'handle the shift already taken'
        UpdateSubForSelf(curShift[0])
        self.redirect(self.uri_for('authenticated'))

    else:
        userTakingShift = User.query().filter(User.email_address==user_email_address).fetch(1)[0]
        curShift[0].status = "closed"
        curShift[0].sub = userTakingShift.key
        curShift[0].put()
        UpdateSubForSelf(curShift[0])
        self.redirect(self.uri_for('authenticated'))

class ClaimSubHandler(BaseHandler):
    '''
    Handle claims for subbing shifts. E-mail the original user about the claim
    '''
    
    @user_required
    def post(self):
        response = json.loads(self.request.body)
        userTakingShift = self.user
        #print response
        ourdatetime = datetime.datetime.strptime(response['shift']['datetime'],'%Y-%m-%dT%H:%M:%S')
        curShift = Shift.query().filter((Shift.datetime == ourdatetime)).fetch(1)
        #print curShift[0].status

        if curShift[0].status != 'open':
          print 'Handle the shift already being taken'
          UpdateSubForSelf(curShift[0])
          self.response.set_status(200)
          self.response.out.write(json.dumps('{success:true,gotshift:false}'))
        else:
          curShift[0].status = "closed"
          sub = User.query().filter(User.email_address==userTakingShift.email_address).fetch(1)[0]
          curShift[0].sub = sub.key
          curShift[0].put()

          #if same user took it, don't send him email - or actually - do.
          UpdateSubForSelf(curShift[0])
          sender_address = "claimedshift@submyshift.appspotmail.com"
          subject = userTakingShift.name + " " + userTakingShift.last_name + " has claimed your shift!"
          body = """ MESSAGE BODY YO """
          mail.send_mail(sender_address, response['shift']['user']['email_address'], subject, body)
          self.response.set_status(200)
          self.response.out.write(json.dumps('{"success":"true","gotshift":"true"}'))

class ImportCalendarHandler(BaseHandler):
  '''
  Handles auth for google calendar importing
  '''

  @decorator.oauth_required
  @user_required
  def get(self):
    service = build('calendar','v3')
    http = decorator.http()
    request = service.calendarList().list()
    allCalendars = request.execute(http =http)
    myCal = None
    for calendar in allCalendars['items']:
      print calendar['summary']
      if calendar['summary'] == 'SubHub':
        myCal = calendar
        break   
    if not myCal:
      self.display_message("AAAAHHH")
    else:
      # Found the calendar to import
      request = service.events().list(calendarId=myCal['id'])
      shifts = request.execute(http=http)
      self.display_message(shifts)

      for shift in shifts['items']:
        user_email = shift['summary']
        starttime = datetime.datetime.strptime(shift['start']['dateTime'],'%Y-%m-%dT%H:%M:%S-04:00')
        endtime = datetime.datetime.strptime(shift['end']['dateTime'],'%Y-%m-%dT%H:%M:%S-04:00')
        diff = endtime - starttime
        duration = (diff.seconds/60)
        cur_user = User.query().filter(User.email_address==user_email).fetch(1)
        newEntry = Shift(sub=None,duration=duration,status="normal", datetime=starttime, user=cur_user[0].key, endtime=endtime)
        newEntry.put()

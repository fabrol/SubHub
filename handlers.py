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
    date = datetime.datetime.now()
    
    mondayDate = WeekStartDate(date.isocalendar()[0], date.isocalendar()[1])
    sundayDate = WeekEndDate(mondayDate)

    mondayofWeek = datetime.datetime.combine(mondayDate, datetime.time(0, 0))
    sundayofWeek = datetime.datetime.combine(sundayDate, datetime.time(23, 0))
    s = Shift.query()
    s = s.filter(Shift.datetime > mondayofWeek)
    s = s.filter(Shift.datetime < sundayofWeek)
    result = shifts_to_dict(s)
    response=json.dumps(result, default=json_object_serializer)
    self.response.out.write(response)
  
  @user_required
  def post(self):
    if not self.request.body:
      date = datetime.datetime.now()
    
      mondayDate = WeekStartDate(date.isocalendar()[0], date.isocalendar()[1])
      sundayDate = WeekEndDate(mondayDate)

      mondayofWeek = datetime.datetime.combine(mondayDate, datetime.time(0, 0))
      sundayofWeek = datetime.datetime.combine(sundayDate, datetime.time(23, 0))
      s = Shift.query()
      s = s.filter(Shift.datetime > mondayofWeek)
      s = s.filter(Shift.datetime < sundayofWeek)
      result = shifts_to_dict(s)
      response=json.dumps(result, default=json_object_serializer)
      self.response.out.write(response)
    else:
      response = json.loads(self.request.body)
      date = datetime.date(response['year'], response['month'] + 1, response['day'])
      
      mondayDate = WeekStartDate(date.isocalendar()[0], date.isocalendar()[1])
      sundayDate = WeekEndDate(mondayDate)

      mondayofWeek = datetime.datetime.combine(mondayDate, datetime.time(0, 0))
      sundayofWeek = datetime.datetime.combine(sundayDate, datetime.time(23, 0))
      s = Shift.query()
      s = s.filter(Shift.datetime > mondayofWeek)
      s = s.filter(Shift.datetime < sundayofWeek)
      result = shifts_to_dict(s)
      response=json.dumps(result, default=json_object_serializer)
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
        ourdatetime = datetime.datetime.strptime(response['shift']['datetime'],'%Y-%m-%dT%H:%M:%S')
        s = '?cur_date_chosen={"month":%d,"day":%d,"year":%d}' %(ourdatetime.month-1,ourdatetime.day,ourdatetime.year)
        subject = str(ourdatetime.strftime("%A, %Y-%m-%d %H:%M:%S"))
        body = ""
        logging.info('Sub request sent by %s', user.email_address)

        # ADD ENCRYPTION FOR SENDING INFO
    
        u = User.query()
        for recipient in u:
            if recipient.email_address is not user.email_address:
                viewlink = self.uri_for('authenticated',_full=True)+s
                claim_url = self.uri_for('claim', user_email=recipient.email_address,
                date_time=response['shift']['datetime'], _full=True)
                mybody = """A new shift has opened up!
click here to view - <a href='%s'> View Shift </a> <br>
click here to claim this shift - <a href='%s'> Claim Shift </a> 
                """ % (viewlink, claim_url)
                print mybody
                mail.send_mail(sender_address,'<'+recipient.email_address+'>', subject, mybody, html = mybody) 
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
        logging.info( 'Another sub request sent for a shift subbed already by %s', cur_sub_user.email_address)
        sender_address = "newshift@submyshift.appspotmail.com"
        ourdatetime = datetime.datetime.strptime(response['shift']['datetime'],'%Y-%m-%dT%H:%M:%S')
        subject = str(ourdatetime.strftime("%A, %Y-%m-%d %H:%M:%S"))
        s = '?cur_date_chosen={"month":%d,"day":%d,"year":%d}' %(ourdatetime.month-1,ourdatetime.day,ourdatetime.year)
        body = ""

        # ADD ENCRYPTION FOR SENDING INFO
    
        u = User.query()
        for recipient in u:
            if recipient.email_address is not cur_sub_user.email_address:
                viewlink = self.uri_for('authenticated',_full=True)+s
                claim_url = self.uri_for('claim', user_email=recipient.email_address,
                date_time=response['shift']['datetime'], _full=True)
                print claim_url
                mybody = """A new shift has opened up!
                click here to view - %s 
                click here to claim - %s
                """ % (viewlink, claim_url)
                print mybody
                mail.send_mail(sender_address, '<'+recipient.email_address+'>', subject, mybody) 
        q = Shift.query()
        curShift = q.filter((Shift.datetime == ourdatetime)).fetch(1)
        curShift[0].status = "open"
        curShift[0].sub = None
        curShift[0].put()
        self.response.set_status(200)
        self.response.out.write(json.dumps('{success:true}'))

def WeekStartDate(year, week):
  d = datetime.date(year, 1, 1)
  delta_days = d.isoweekday() - 1
  delta_weeks = week
  if year == d.isocalendar()[0]:
    delta_weeks -=1
  delta = datetime.timedelta(days=-delta_days, weeks=delta_weeks)
  return d + delta
def WeekEndDate(monday):
  delta_sunday = datetime.timedelta(days=6)
  return monday + delta_sunday

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
    logging.info('Sub claimed by  %s for shift', user_email_address, shift_datetime)
    ourdatetime = datetime.datetime.strptime(shift_datetime,'%Y-%m-%dT%H:%M:%S')
    curShift = Shift.query().filter(Shift.datetime == ourdatetime).fetch(1)
    
    s = '?cur_date_chosen={"month":%d,"day":%d,"year":%d}' %(ourdatetime.month-1,ourdatetime.day,ourdatetime.year)
    print s
    if curShift[0].status != 'open':
        print 'handle the shift already taken'
        UpdateSubForSelf(curShift[0])
        self.redirect(self.uri_for('authenticated')+s)

    else:
        userTakingShift = User.query().filter(User.email_address==user_email_address).fetch(1)[0]
        curShift[0].status = "closed"
        curShift[0].sub = userTakingShift.key
        curShift[0].put()
        UpdateSubForSelf(curShift[0])
        self.redirect(self.uri_for('authenticated')+s)

class ClaimSubHandler(BaseHandler):
    '''
    Handle claims for subbing shifts. E-mail the original user about the claim
    '''
    
    @user_required
    def post(self):
        response = json.loads(self.request.body)
        userTakingShift = self.user
        ourdatetime = datetime.datetime.strptime(response['shift']['datetime'],'%Y-%m-%dT%H:%M:%S')
        logging.info('Sub claimed by %s for shift at %s', userTakingShift.email_address, ourdatetime)
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
          body = """ """
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
		manager = self.user
		if not self.user.isManager:
			self.display_message("Sorry, but you are not authorized to import calendars")	
		else:
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
				self.display_message("Something went wrong! Try and correctly format the google calendar and try again!")
			else:
				# Found the calendar to import
				request = service.events().list(calendarId=myCal['id'])
				shifts = request.execute(http=http)

				for shift in shifts['items']:
					user_email = shift['summary']
					starttime = datetime.datetime.strptime(shift['start']['dateTime'],'%Y-%m-%dT%H:%M:%S-04:00')
					endtime = datetime.datetime.strptime(shift['end']['dateTime'],'%Y-%m-%dT%H:%M:%S-04:00')
					diff = endtime - starttime
					duration = (diff.seconds/60)
					cur_user = User.query().filter(User.email_address==user_email).fetch(1)
					print user_email
					newEntry = Shift(sub=None,duration=duration,status="normal", datetime=starttime, user=cur_user[0].key, endtime=endtime)
					newEntry.put()
			logging.info('Manager calendar imported')
			self.redirect(self.uri_for('authenticated'))

class ManagerViewHandler(BaseHandler):
  @user_required
  def get(self):  
      self.render_template('managerview.html')

class GetManagerShifts(BaseHandler):
  '''
  Handles the manager view
  '''

  @user_required
  def post(self):
    manager = self.user
    if not self.user.isManager:
      self.display_message("Sorry, but you are not authorized to import calendars") 
    else:
      # Show each user and with each user show the normal shifts, subbed shifts and subs asked for (maybe in a date range?)
      u = User.query()
      s = Shift.query()

      result = {}
      for user in u:
        reg_shifts = 0
        asked_sub_shifts = 0
        subbing = 0
        for shift in s.filter(Shift.user==user.key):
          reg_shifts += 1
          if shift.status == 'open':
            asked_sub_shifts += 1
        for shift in s.filter(Shift.sub==user.key):
          subbing += 1
        shifts = {'reg_shifts':reg_shifts,'asked_sub_shifts':asked_sub_shifts,'subbing':subbing}
        #shifts = shifts_to_dict(s.filter(Shift.user == user.key))
        result[user.email_address] = shifts
      response=json.dumps(result, default=json_object_serializer)
      self.response.out.write(response)


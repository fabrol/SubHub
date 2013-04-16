#!/usr/bin/env python

from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

import os.path
import webapp2
import routes
import logging
import config as app_config
from webapp2_extras import auth
from webapp2_extras import sessions

app = webapp2.WSGIApplication(
debug=True, config=app_config.config)

routes.add_routes(app)

logging.getLogger().setLevel(logging.DEBUG)

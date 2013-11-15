#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
import os
import logging
import jinja2
import webapp2
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class Transaction(ndb.Model):
  """Models an individual Transaction entry with content and date."""
  content = ndb.StringProperty()
  vendor = ndb.StringProperty()
  position = ndb.GeoPtProperty()
  amount = ndb.StringProperty()
  #date = ndb.DateTimeProperty(auto_now_add=True)

class CounterWorker(webapp2.RequestHandler):
    def post(self): # should run at most 1/s
        #content = self.request.get('content')
        #vendor = self.request.get('vendor')
        #amount = self.request.get('amount')
        #logging.info("Working " + content + " - " + vendor + " - " + amount)
		logging.info("Working ")

		transaction=Transaction(
			parent=ndb.Key("Transaction", "Svesse" or "*notitle*"), 
			content=self.request.get('content'),
			vendor=self.request.get('vendor'),
			amount=self.request.get('amount'),
			position = ndb.GeoPt(52.37, 4.88)
		)

		transaction.put()

#        def txn():
#            counter = Counter.get_by_key_name(key)
#            if counter is None:
#                counter = Counter(key_name=key, count=1)
#            else:
#                counter.count += 1
#            counter.put()
#        db.run_in_transaction(txn)

class MainPage(webapp2.RequestHandler):

    def get(self):
		template_values = {
			'greetings': 'zxc',
		}
		template = JINJA_ENVIRONMENT.get_template('js.html')
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/worker', CounterWorker),('/j', MainPage),], debug=True)
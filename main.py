#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
import json  
import endpoints

from google.appengine.api import app_identity
from google.appengine.ext import ndb
from protorpc import messages
from protorpc import message_types
from protorpc import remote

class Transaction(ndb.Model):
  """Models an individual Transaction entry with content and date."""
  content = ndb.StringProperty()
  vendor = ndb.StringProperty()
  position = ndb.GeoPtProperty()
  amount = ndb.FloatProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

class TransactionCollection(messages.Message):
    """Collection of Transactions."""
    items = messages.MessageField(Transaction, 1, repeated=True)  

@endpoints.api(name='trans2', version='v1')
class MainHandler(remote.Service):

  @endpoints.method(message_types.VoidMessage, TransactionCollection,path='allTransactions', http_method='GET',name='transactions.listTransactions')
  def transaction_list(self, unused_request):
    ancestor_key=ndb.Key("Transaction", "Svesse" or "*notitle*")
    transactions = Transaction.query_book(ancestor_key).fetch(20)

  def get(self):
    self.response.write('Hello world!')
    logging.debug("value of my var is")
    logging.info("info" + app_identity.get_application_id())

  def post(self):
  	transaction=Transaction(
  		parent=ndb.Key("Transaction", "Svesse" or "*notitle*"), 
  		content=self.request.get('content'),
  		vendor=self.request.get('vendor'),
  		amount=float(self.request.get('amount')),
  		position = ndb.GeoPt(52.37, 4.88)
  	)
  	transaction.put()


#app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)

APPLICATION = endpoints.api_server([MainHandler])
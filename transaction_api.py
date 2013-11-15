"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""
import logging
import endpoints
from google.appengine.api import app_identity
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
from protorpc import messages
from protorpc import message_types
from protorpc import remote


package = 'BoldResult'


class Transaction(messages.Message):
    """Transaction that stores a message."""
    content = messages.StringField(1)
    vendor = messages.StringField(2)
    amount = messages.StringField(3)


class TransactionCollection(messages.Message):
    """Collection of Transactions."""
    items = messages.MessageField(Transaction, 1, repeated=True)


STORED_TRANSACTIONS = TransactionCollection(items=[
    Transaction(content='0 Transaction world!', amount="123"),
    Transaction(content='zzz', vendor='1 goodbye Transaction!', amount="33"),
])


@endpoints.api(name='trans', version='v2',description='A transaction api_server')
class TransactionApi(remote.Service):
    """Transactions API v2."""
    
    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(Transaction,uid=messages.IntegerField(2, variant=messages.Variant.INT32,required=True))
    #MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(Transaction)
    @endpoints.method(MULTIPLY_METHOD_RESOURCE, Transaction, path='queueIt/{uid}', http_method='POST', name='transactions.queueTransaction')
    def transactions_queueTransaction(self, request):
        """Use this method to post transactions"""
        taskqueue.add(queue_name='transactionQueue', url='/worker', params={'content': request.content, 'vendor':request.vendor, 'amount':request.amount})
        return Transaction(content=request.content, amount=request.amount, vendor=request.vendor)


    @endpoints.method(message_types.VoidMessage, TransactionCollection,path='allTransactions', http_method='GET',name='transactions.listTransactions')
    def transaction_list(self, unused_request):
        logging.info("Return all transactions")
        return STORED_TRANSACTIONS



    ID_RESOURCE = endpoints.ResourceContainer(message_types.VoidMessage,id=messages.IntegerField(1, variant=messages.Variant.INT32))
    @endpoints.method(ID_RESOURCE, Transaction,path='aTransaction/{id}', http_method='GET',name='transactions.getTransaction')
    def transaction_get(self, request):
        try:
            return STORED_TRANSACTIONS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Transaction %s not found.' %
                                              (request.id,))

APPLICATION = endpoints.api_server([TransactionApi])
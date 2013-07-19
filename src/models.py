'''
Created on 18/07/2013

@author: guillem
'''

from google.appengine.ext import ndb

class Form(ndb.Model):
    '''    
    Models a bet form
    '''
    creator = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    fields = ndb.JsonProperty(Required=True)


class Bet(ndb.Model):
    '''
    Models a bet
    '''
    user = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    fields = ndb.JsonProperty(required=True)
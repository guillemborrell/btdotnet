'''
Created on Jul 20, 2013

@author: guillem
'''
from twython import Twython
from google.appengine.ext import ndb


class Session(ndb.Model):
    oauth_token = ndb.StringProperty()
    oauth_token_secret = ndb.StringProperty()
    oauth_verifier = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    
    

class OAuth(object):
    def __init__(self,callback_url):

        self.twitter = Twython(self.APP_KEY, self.APP_SECRET)
        self.callback_url = callback_url
        self.auth = None
        
    def get_tokens(self):
        self.auth = self.twitter.get_authentication_tokens(self.callback_url)

'''
Created on Jul 20, 2013

@author: guillem
'''
from twython import Twython


class OAuth(object):
    def __init__(self,callback_url):
        self.APP_KEY = 'dmyD2CHHePKQ6M7bQJg3wQ'
        self.APP_SECRET = 'tAsyLFGu9GIuYluUbNjqmv29Cg0VifK5w8yIKFrmo'
        self.twitter = Twython(self.APP_KEY, self.APP_SECRET)
        self.callback_url = callback_url
        self.auth = None
        
    def get_tokens(self):
        self.auth = self.twitter.get_authentication_tokens(self.callback_url)
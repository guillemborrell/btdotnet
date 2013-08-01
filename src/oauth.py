'''
Created on Jul 20, 2013

@author: guillem
'''
from twython import Twython
from google.appengine.ext import ndb

APP_KEY = 'dmyD2CHHePKQ6M7bQJg3wQ'
APP_SECRET = 'tAsyLFGu9GIuYluUbNjqmv29Cg0VifK5w8yIKFrmo'


def session_auth(session,request,this_url):
    #Function that manages the session status.
    if session.get('key'):
        #If the cookie is found, get the key and look for the session data in the database
        session_data = ndb.Key(urlsafe = session.get('key')).get()
            
        #If the page is visited from the twitter authentication callback, it will receive the oauth_verifier parameter
        if request.get('oauth_verifier'):
            oauth_verifier = request.get('oauth_verifier')
            oauth_token = request.get('oauth_token')
            twitter = Twython(APP_KEY, APP_SECRET,
                              session_data.oauth_token,
                              session_data.oauth_token_secret)
        
                #The twitter authentication returns oauth_token, and it is compared with the original token
            if session_data.oauth_token == oauth_token:
                final_step = twitter.get_authorized_tokens(oauth_verifier)
                session_data.oauth_token = final_step['oauth_token']
                session_data.oauth_token_secret = final_step['oauth_token_secret']
                session_data.oauth_verifier = oauth_verifier
                auth = Twython(APP_KEY, APP_SECRET,
                               session_data.oauth_token,
                               session_data.oauth_token_secret)
                credentials = auth.verify_credentials()
                session_data.username = credentials['screen_name']
                session_data.name = credentials['name']
                session_data.avatar = credentials['profile_image_url']
                key = session_data.put()
                session['key'] = key.urlsafe()
                return 'LOGGED_IN', credentials
                    
            # If the tokens are not equal, an exception is raised.
            else:
                return 'ERROR', None
        
        elif session_data.oauth_verifier:
            # auth = Twython(APP_KEY, APP_SECRET,
            # session_data.oauth_token,
            # session_data.oauth_token_secret)
            # credentials = auth.verify_credentials()
            credentials = {'screen_name': session_data.username,
                           'name': session_data.name,
                           'profile_image_url': session_data.avatar}
            return 'LOGGED_IN', credentials
        
        else:
            twitter  = Twython(APP_KEY, APP_SECRET)
            auth = twitter.get_authentication_tokens(this_url)
            session_data = Session(oauth_token = auth['oauth_token'],
                                   oauth_token_secret = auth['oauth_token_secret'])
            key = session_data.put()
            session['key'] = key.urlsafe()
            return 'ANONYMOUS', auth['auth_url']
        
    else:
        twitter  = Twython(APP_KEY, APP_SECRET)
        auth = twitter.get_authentication_tokens(this_url)
        session_data = Session(oauth_token = auth['oauth_token'],
                               oauth_token_secret = auth['oauth_token_secret'])
        key = session_data.put()
        session['key'] = key.urlsafe()
        return 'ANONYMOUS', auth['auth_url']
    

class Session(ndb.Model):
    oauth_token = ndb.StringProperty()
    oauth_token_secret = ndb.StringProperty()
    oauth_verifier = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    avatar = ndb.StringProperty()

   
def check_username(key,username):
    session = ndb.Key(url_safe=key).get()
    return session.username == username


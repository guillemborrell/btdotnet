import webapp2
import logging
from google.appengine.ext.webapp.util import run_wsgi_app

from webapp2_extras import sessions
from oauth import Session
from twython import Twython
from google.appengine.ext import ndb

APP_KEY = 'dmyD2CHHePKQ6M7bQJg3wQ'
APP_SECRET = 'tAsyLFGu9GIuYluUbNjqmv29Cg0VifK5w8yIKFrmo'


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        
        try:
            webapp2.RequestHandler.dispatch(self)
        
        finally:
            self.session_store.save_sessions(self.response)
        
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()


class MainPage(BaseHandler):     
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('''
        <html>
        <body>
        <p>Hello, World!</p>
        ''')

        if self.session.get('key'):
            session_data = ndb.Key(urlsafe = self.session.get('key')).get()
            
            if self.request.get('oauth_verifier'):
                oauth_verifier = self.request.get('oauth_verifier')
                oauth_token = self.request.get('oauth_token')
                twitter = Twython(APP_KEY, APP_SECRET,
                                  session_data.oauth_token,
                                  session_data.oauth_token_secret)
                logging.info(session_data.oauth_token)
                logging.info(oauth_token)
                logging.info(oauth_verifier)
                final_step = twitter.get_authorized_tokens(oauth_verifier)
                session_data.oauth_token = final_step['oauth_token']
                session_data.oauth_token_secret = final_step['oauth_token_secret']
                session_data.oauth_verifier = oauth_verifier
                key = session_data.put()
                self.session['key'] = key.urlsafe()
                self.response.out.write('<p>You are now successfully authenticated. Please go <a href="http://betweetdotnet.appspot.com">here</a></p>')
                
                
            elif session_data.oauth_verifier:
                auth = Twython(APP_KEY, APP_SECRET,
                               session_data.oauth_token,
                               session_data.oauth_token_secret)
                credentials = auth.verify_credentials()
                self.response.out.write('<p>You are logged in as {}, <img src="{}" width="25px"</p>'.format(
                    credentials['screen_name'],
                    credentials['profile_image_url']))
            
            
            else:
                twitter  = Twython(APP_KEY, APP_SECRET)
                auth = twitter.get_authentication_tokens('http://betweetdotnet.appspot.com')
                session_data = Session(oauth_token = auth['oauth_token'],
                                       oauth_token_secret = auth['oauth_token_secret'])
                key = session_data.put()
                self.session['key'] = key.urlsafe()
                self.response.out.write('<p><a href="{}">Login</a></p>'.format(auth['auth_url']))        
                                    
            
        else:
            #No session information
            # Landing from authentication
            twitter  = Twython(APP_KEY, APP_SECRET)
            auth = twitter.get_authentication_tokens('http://betweetdotnet.appspot.com')
            session_data = Session(oauth_token = auth['oauth_token'],
                                   oauth_token_secret = auth['oauth_token_secret'])
            key = session_data.put()
            self.session['key'] = key.urlsafe()
            self.response.out.write('<p><a href="{}">Login</a></p>'.format(auth['auth_url']))        

#             
        self.response.out.write('''
        </body>
        </html>''')

        
    def post(self):
        print self.request.get('arg')

config ={}
config['webapp2_extras.sessions'] = {
    'secret_key': 'tAsyLFGu9GIuYluUbNjqmv29Cg0VifK5w8yIKFrmp',
    'cookie_name': 'betweet_session',
    'cookie_args': {'max_age': 30*24*3600},
    }

application = webapp2.WSGIApplication([
    ('/', MainPage)], debug=True, config = config)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

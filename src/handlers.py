# Handlers for forms and bets.
import webapp2
from webapp2_extras import sessions
from oauth import session_auth


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
        auth, var = session_auth(
            self.session,
            self.request, 
            'http://betweetdotnet.appspot.com')


        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('''
        <html>
        <body>
        <p>Hello, World!</p>
        ''')

        if auth == 'ANONYMOUS':
            self.response.out.write('<p><a href="{}">Log in</a></p>'.format(var))
        elif auth == 'LOGGED_IN':
            self.response.out.write('<p>Logged in as {}</p>'.format(var['screen_name']))
        else:
            self.response.out.write('<p>Something wrong happened {}</p>'.format(auth))
        self.response.out.write('''
        </body>
        </html>''')

        
    def post(self):
        print self.request.get('arg')
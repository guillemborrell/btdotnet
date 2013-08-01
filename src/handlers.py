# Handlers for forms and bets.
import webapp2
import jinja2
import os
from webapp2_extras import sessions
from oauth import session_auth


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])   


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


class FormPage(BaseHandler):     
    def get(self):
        auth, var = session_auth(
            self.session,
            self.request, 
            'http://betweetdotnet.appspot.com/new')
 
        template_values = {'auth': auth,
                           'var': var,
                           'key': self.session.get('key')
                           }
 
        template = JINJA_ENVIRONMENT.get_template('./templates/genform.html')
        self.response.write(template.render(template_values))
         
    def post(self):
        print self.request.get('arg')
        

class EntryPage(BaseHandler):
    def get(self):
        auth, var = session_auth(
            self.session,
            self.request,
            'http://betweetdotnet.appspot.com')
        
        template_values = {'auth': auth,
                           'var': var,
                           'key': self.session.get('key')
                           }
        template = JINJA_ENVIRONMENT.get_template('./templates/index.html')
        self.response.write(template.render(template_values))
        
                    

class LogoutPage(BaseHandler):
    def get(self):
        auth, var = session_auth(
            self.session,
            self.request,
            'http://betweetdotnet.appspot.com/logout'
            )
        
        key = self.session.get('key')
        
        self.session['key'] = ''
        
        template_values = {'auth': auth,
                           'var': var,
                           'key': key
                           }
        template = JINJA_ENVIRONMENT.get_template('./templates/logout.html')
        self.response.out.write(template.render(template_values))
        
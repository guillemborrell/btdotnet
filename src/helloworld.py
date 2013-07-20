from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import oauth

from oauth import OAuth


class MainPage(webapp.RequestHandler): 
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('''
        <html>
        <body>
        <p>Hello, webapp World!</p>
        ''')

        auth = OAuth('http://betweetdotnet.appspot.com')       
        auth.get_tokens()
        self.response.out.write('<p><a href="{}">Login</a></p>'.format(auth.auth['auth_url']))
#             
        self.response.out.write('''
            </body>
            </html>''')

        
    def post(self):
        print self.request.get('arg')


application = webapp.WSGIApplication([
    ('/', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

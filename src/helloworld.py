from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import oauth

from login import OAuthHandler, OAuthClient


class MainPage(webapp.RequestHandler): 
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('''
        <html>
        <body>
        <p>Hello, webapp World!</p>
        ''')

        client = OAuthClient('twitter', self)       
            
        if not client.get_cookie():
            self.response.out.write('''
                <p><a href="/oauth/twitter/login">Login via Twitter</a> {}</p>
                '''.format(client.get_cookie()))
#             self.response.out.write('''
#             </body>
#             </html>''')
            
            
        try:
            user = oauth.get_current_user()
            self.response.write('<p>{}</p>'.format(user.nickname()))
            
        except oauth.OAuthRequestError:
            self.response.write('<p>no oauuuuuuuuuth</p>')
        
            
        self.response.out.write(
            '<a href="/oauth/twitter/logout">Logout from Twitter</a><br /><br />'
            )
        
#         info = client.get('/account/verify_credentials')
#         
#         self.response.out.write("<p>Screen name: {}</p>".format(info["screen_name"]))
#         self.response.out.write("<p>Location: {}</p>".format(info["location"]))
#             
        self.response.out.write('''
            </body>
            </html>''')

        
    def post(self):
        print self.request.get('arg')


application = webapp.WSGIApplication([
    ('/oauth/(.*)/(.*)', OAuthHandler),
    ('/', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

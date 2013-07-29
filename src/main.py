import webapp2

from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import EntryPage, FormPage
from rest import FormView, FormFromCreator, FormLastBets, FormAllBets

config ={}
config['webapp2_extras.sessions'] = {
    'secret_key': 'tAsyLFGu9GIuYluUbNjqmv29Cg0VifK5w8yIKFrmp',
    'cookie_name': 'betweet_session',
    'cookie_args': {'max_age': 30*24*3600},
    }

application = webapp2.WSGIApplication(
    [
     ('/', EntryPage),
     ('/new', FormPage),
     ('/form', FormView),
     ('/form/fromcreator', FormFromCreator),
     ('/form/lastbets', FormLastBets),
     ('/form/allbets', FormAllBets),
     ], debug=True, config = config)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

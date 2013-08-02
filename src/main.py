import webapp2

from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import EntryPage, FormPage, ViewFormPage, LogoutPage
from rest import FormView, FormFromCreator, FormLastBets, FormAllBets, BetView, BetFromUser

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
     ('/logout', LogoutPage),
     ('/viewform', ViewFormPage),
     ('/restform', FormView),
     ('/restform/fromcreator', FormFromCreator),
     ('/restform/lastbets', FormLastBets),
     ('/restform/allbets', FormAllBets),
     ('/restbet', BetView),
     ('/restbet/fromuser', BetFromUser),
     ], debug=True, config = config)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

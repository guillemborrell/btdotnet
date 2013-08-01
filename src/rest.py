# -*- coding: utf-8 -*-

import webapp2
import datetime
import json
from models import Form
from google.appengine.ext import ndb
import logging

class FormView(webapp2.RequestHandler):
    def get(self):
        if self.request.get('key'):
            form = ndb.Key(urlsafe = self.request.get('key')).get()
            if form:
                self.response.headers['Content-Type'] = 'application/json'
                self.response.out.write(json.dumps(form.to_dict_key()))
            else:
                self.abort(404)
        else:
            self.abort(404)
        
    def post(self):
        logging.info(self.request.body)
        try:
            jsondata = json.loads(self.request.body)
        except UnicodeDecodeError:
            jsondata = json.loads(self.request.body,encoding='latin-1')

        logging.info(jsondata.keys())

        form = Form()
        
        form.creator = jsondata['creator']
        form.until = datetime.datetime.now() + datetime.timedelta(hours=jsondata['duration'])
        form.hashtag = jsondata['hashtag']
        form.fields = jsondata['fields']
        form.description = jsondata['description']
        form.authenticated = bool(jsondata['authenticated']) 

        form.put()
        
        
class FormFromCreator(webapp2.RequestHandler):
    def get(self):
        if self.request.get('creator'):
            creator = self.request.get('creator')
            forms = Form.from_creator(creator)
        
            if forms:
                betslist = json.dumps([f.to_dict_key() for f in forms])
                self.response.headers['Content-Type'] = 'application/json'
                self.response.out.write(betslist)
            else:
                self.abort(404)
        else:
            self.abort(404)
                           

class FormLastBets(webapp2.RequestHandler):
    def get(self):
        if self.request.get('key'):
            form = ndb.Key(urlsafe=self.request.get('key')).get()
            if form:
                bets = form.last_bets()
                if bets:
                    betslist = json.dumps([b.to_dict_key() for b in bets])
                    self.response.headers['Content-Type'] = 'application/json'
                    self.response.out.write(betslist)
                else:
                    self.abort(404)                    
            else:
                self.abort(404)
        else:
            self.abort(404)

                   
class FormAllBets(webapp2.RequestHandler):
    def get(self):
        if self.request.get('key'):
            form = ndb.Key(urlsafe = self.request.get('key')).get()
            if form:
                bets = form.all_bets()

                if bets:
                    betslist = json.dumps([b.to_dict_key() for b in bets])
                    self.response.headers['Content-Type'] = 'application/json'
                    self.response.out.write(betslist)
            
                else:
                    self.abort(404)
            else:
                self.abort(404)
        else:
            self.abort(404)    

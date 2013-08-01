'''
Created on 18/07/2013

@author: guillem
'''

from google.appengine.ext import ndb

class Form(ndb.Model):
    '''    
    Models a bet form
    '''
    creator = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    until = ndb.DateTimeProperty(required=True)
    hashtag= ndb.StringProperty(required=True)
    fields = ndb.JsonProperty(required=True)
    authenticated = ndb.BooleanProperty(required=True)

    def to_dict_key(self):
        d = {}
        d['key'] = self.key.urlsafe()
        d['creator'] = self.creator
        d['description'] = self.description
        d['time'] = self.time.isoformat()
        d['until'] = self.until.isoformat()
        d['hashtag'] = self.hashtag
        d['fields'] = self.fields
        d['authenticated'] = self.authenticated
        d['bets'] = self.number_of_bets()
        
        return d
        
    @classmethod
    def from_creator(cls,name):
        return cls.query(
            cls.creator == name
            ).order(-cls.time).fetch(5)
    
    def number_of_bets(self):
        return Bet.count_form(self.key)

    def last_bets(self, num=10):
        return Bet.query_form(self.key, num=num)
    
    def all_bets(self):
        return Bet.query_form_any(self.key)
    
    def authenticated_bets(self):
        return Bet.query_form_auth(self.key)
    
    @classmethod
    def popular(cls, num=10):
        return cls.query().order(cls.number_of_bets()).fetch(num)


class Bet(ndb.Model):
    '''
    Models a bet. Parent is the Form
    '''
    user = ndb.StringProperty(required=True)
    authenticated = ndb.BooleanProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    fields = ndb.JsonProperty(required=True)
    
    @classmethod
    def to_dict_key(cls):
        d = {}
        d['user'] = cls.user
        d['authenticated'] = cls.authenticated
        d['time'] = cls.time.isoformat()
        d['fields'] = cls.fields
        
        return d
    
    @classmethod
    def query_form(cls, ancestor_key, num=10):
        return cls.query(
            ancestor=ancestor_key
            ).order(-cls.time).fetch(10)
    
    @classmethod
    def count_form(cls, ancestor):
        return cls.query(ancestor=ancestor).count()
    
    @classmethod
    def query_form_any(cls, ancestor_key):
        "Returns all bets. First is first"
        return cls.query(
            ancestor=ancestor_key             
            ).order(cls.date).fetch(
                cls.count_form(ancestor_key)
                )
    
    @classmethod
    def query_form_auth(cls, ancestor_key):
        "Returns authenticaded bets. First is first"
        return cls.query(
            ancestor=ancestor_key
            ).filter(
                cls.authenticated==True
                ).order(cls.date).fetch(
                    cls.count_form(ancestor_key)
                    )

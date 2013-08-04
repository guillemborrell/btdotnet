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
    info = ndb.TextProperty()

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
        d['info'] = self.info
        d['bets'] = self.number_of_bets()
        
        return d
        
    @classmethod
    def from_creator(cls,name,num=5):
        return cls.query(
            cls.creator == name
            ).order(-cls.time).fetch(num)
    
    @classmethod
    def last(cls,num=5):
        return cls.query().order(-cls.time).fetch(num)
    
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
    description = ndb.StringProperty(required=True)
    user = ndb.StringProperty(required=True)
    authenticated = ndb.BooleanProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    fields = ndb.JsonProperty(required=True)

    @classmethod
    def from_user(cls,name):
        return cls.query(
            cls.user == name
            ).filter(cls.authenticated==True).order(-cls.time).fetch(5)
    
    def to_dict_key(self):
        d = {}
        d['key'] = self.key.urlsafe()
        d['user'] = self.user
        d['authenticated'] = self.authenticated
        d['time'] = self.time.isoformat()
        d['fields'] = self.fields
        d['description'] = self.description
        
        return d
    
    @classmethod
    def query_form(cls, ancestor_key, num=10):
        try:
            bets = cls.query(
                ancestor=ancestor_key
                ).order(-cls.time).fetch(10)
        except NeedIndexError:
            bets = []
        return bets
    
    @classmethod
    def count_form(cls, ancestor):
        return cls.query(ancestor=ancestor).count()
    
    @classmethod
    def query_form_any(cls, ancestor_key):
        "Returns all bets. First is first"
        return cls.query(
            ancestor=ancestor_key             
            ).order(cls.time).fetch(
                cls.count_form(ancestor_key)
                )
    
    @classmethod
    def query_form_auth(cls, ancestor_key):
        "Returns authenticaded bets. First is first"
        return cls.query(
            ancestor=ancestor_key
            ).filter(
                cls.authenticated==True
                ).order(cls.time).fetch(
                    cls.count_form(ancestor_key)
                    )


class Session(ndb.Model):
    oauth_token = ndb.StringProperty()
    oauth_token_secret = ndb.StringProperty()
    oauth_verifier = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    credentials = ndb.JsonProperty()

    @property
    def username(self):
        return self.credentials['screen_name']
    
    @property
    def name(self):
        return self.credentials['name']
    
    @property
    def avatar(self):
        return self.credentials['profile_image_url']
    
    @property
    def lang(self):
        return self.credentials['lang']
    
    @property
    def verified(self):
        return self.credentials['verified']
    
    @classmethod
    def last_from_username(cls, username):
        return cls.query(
            cls.username == username
                ).order(-cls.time).fetch(1)


class Profile(ndb.Model):
    time=ndb.DateTimeProperty(auto_now_add=True)
    name=ndb.StringProperty(required=True)
    reputation=ndb.IntegerProperty(required=True)

    def to_dict_key(self):
        d={}
        d['key'] = self.key.urlsafe()
        d['time'] = self.time
        d['name'] = self.name
        d['reputation'] = self.reputation

    def last_session(self):
        return Session.last_from_username(self.name)
    
    @classmethod
    def from_name(cls, name):
        return cls.query(cls.name == name).fetch(1)  
        

class Comment(ndb.Model):
    """Parent has to be Profile"""
    author=ndb.StringProperty(required=True)
    vote=ndb.IntegerProperty(required=True)
    text=ndb.StringProperty()

    
class Template(ndb.Model):
    """Templates for bets"""
    description=ndb.StringProperty(required=True)
    value=ndb.StringProperty(required=True)

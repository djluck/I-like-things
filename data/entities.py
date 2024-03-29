from google.appengine.ext import db
import google.appengine.api.users
import datetime
import config

class Owner(db.Model):
    user = db.UserProperty(required=True, auto_current_user_add=True)

class Entry(db.Model):
    link = db.LinkProperty(required=True)
    date_created = db.DateTimeProperty(required=True, auto_now=True)
    date_expires = db.DateProperty()
    
    @property
    def tags(self):
        q = Tag.all()
        q.filter("entries_tagged =", self)
        return q.fetch(config.max_tags_per_entry)
    
class Tag(db.Model):
    entries_tagged = db.ListProperty(db.Key)
    date_created = db.DateTimeProperty(required=True, auto_now=True)
    last_used = db.DateTimeProperty(required=True, auto_now=True)
    times_used = db.IntegerProperty(default=0)
    
    @property
    def value(self):
        return self.key().name()    
    
    def __str__(self):
        return self.key().name()
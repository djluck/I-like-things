from google.appengine.ext import db
import google.appengine.api.users
import datetime

class User(db.Model):
    user = db.UserProperty(required=True, auto_current_user_add=True)

class Entry(db.Model):
    link = db.LinkProperty(required=True)
    date_created = db.DateTimeProperty(required=True, auto_now=True)
    date_expires = db.DateProperty()
    
class Tag(db.Model):
    entries_tagged = db.ListProperty(db.Key)
    date_created = db.DateTimeProperty(required=True, auto_now=True)
    last_used = db.DateTimeProperty(required=True, auto_now=True)
    
    def __str__(self):
        return self.key().name()
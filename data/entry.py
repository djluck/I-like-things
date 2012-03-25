from google.appengine.ext import db
import google.appengine.api.users
import datetime

class Entry(db.Model):
    
    link = db.LinkProperty(required=True)
    date_created = db.DateTimeProperty(required=True, auto_now=True)
    date_expires = db.DateProperty()
    user = db.UserProperty(required=True, auto_current_user_add=True)
    tags = db.ListProperty(db.Category)
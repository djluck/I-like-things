from google.appengine.ext import db
import datetime

class Entry(db.Model):
    link = db.LinkProperty
    date_created = db.DateTimeProperty
    date_expires = db.DateProperty
    user = db.UserProperty
    tags = ListProperty(db.CategoryType)
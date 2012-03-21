import webapp2
from handlers.base import Base
from google.appengine.ext import db
from entities.entry import Entry
from google.appengine.api import users

class List(Base):
    def get(self):
        q = Entry.all();
        q.filter("user = ", users.get_current_user())
        q.order("-date_created")
        template_values = {
            "user": users.get_current_user(),
            "entries" : q.fetch(50)
        }
        
        self.render_template("list.html",  template_values)

app = webapp2.WSGIApplication([('/.*', List)],
                              debug=True)
import webapp2
from handlers.base import Base
from google.appengine.ext import db
from data.functions import get_recent_entries, get_all_tags
from google.appengine.api import users

class List(Base):
    def get(self):
        template_values = {
            "user": users.get_current_user(),
            "recent_entries" : get_recent_entries(),
            "tags" : [t.value for t in get_all_tags()]
        }
        
        self.render_template("list.html",  template_values)

app = webapp2.WSGIApplication([('/.*', List)],
                              debug=True)
import webapp2
from handlers.base import Base
from google.appengine.ext import db

class List(Base):
    def get(self):
        template_values = {
            "name":"james"
        }
        self.render_template("list.html",  template_values)

app = webapp2.WSGIApplication([('/.*', List)],
                              debug=True)
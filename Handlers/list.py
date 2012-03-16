import webapp2
from Handlers.base import Base

class List(Base):
    def get(self):
        self.render_template("list.html",  {"myname":"JAMES"})

app = webapp2.WSGIApplication([('/.*', List)],
                              debug=True)
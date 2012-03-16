import webapp2
from handlers.base import Base
from entities.entry import Entry

class Add(Base):
    def get(self):
        self.render_template("add.html",  {"myname":"JAMES"})
        
    def post(self):
        entry = Entry(link=self.request.get('link'))
        entry.put()
        self.render_template("add.html",  {"added" : True, "link" : entry.link})

app = webapp2.WSGIApplication([('/new', Add)],
                              debug=True)
import webapp2
from handlers.base import Base
from entities.entry import Entry
from google.appengine.ext import db

class Add(Base):
    def get(self):
        result =  Entry.all().fetch(100)
        tags = [i for i in set([t for e in result for t in e.tags])]
        self.render_template("add.html", {"tags" : tags})
        
    def post(self):
        entry = Entry(link=self.request.get("link"), tags = [db.Category(x) for x in self.request.get("tags").split(" ")])
        entry.put()
        self.render_template("add.html",  {"added" : True, "link" : entry.link})

app = webapp2.WSGIApplication([('/new', Add)],
                              debug=True)
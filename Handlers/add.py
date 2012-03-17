import webapp2
from handlers.base import Base
from entities.entry import Entry
from google.appengine.ext import db
from datetime import datetime

class Add(Base):
    def get(self):
        self.render_initial()
        
    def post(self):
        link = self.request.get("link")
        if link[0:4] != "http":
            link = "http://" + link
        date_expires = self.request.get("date_expires")
        if date_expires != "":
            date_expires = datetime.strptime(date_expires, "%d/%m/%y").date()
        else:
            date_expires = None
        tags = [db.Category(x) for x in self.request.get("tags").split(" ")]
        entry = Entry(link=link, 
                      tags = tags,
                      date_expires = date_expires)
        entry.put()
        
        self.render_initial(additional_values={"added" : True, "link" : entry.link})
        
    def render_initial(self, additional_values=None):
        result =  Entry.all().fetch(100)
        tags = [i for i in set([t for e in result for t in e.tags])]
        self.render_template("add.html", {"tags" : tags})  
        
        
app = webapp2.WSGIApplication([('/new', Add)],
                              debug=True)
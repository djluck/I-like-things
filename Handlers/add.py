import webapp2
from handlers.base import Base
from entities.entry import Entry
from google.appengine.ext import db
from datetime import datetime
import urlparse

class Add(Base):
    def get(self):
        template_values = {}
        if (self.request.get("added") != ""):
            template_values["added"] = True        
        self.render_initial(template_values)
        
    def post(self):
        errors = []
        
        link = self.request.get("link").strip(" ")
        if len(link) > 0 and link[0:4] != "http":
            link = "http://" + link
        if len(link) == 0:
            errors.append("Link must not be empty")
        elif not reduce(lambda x, y: (len(y) > 0) and x, urlparse.urlparse(link), True):
            errors.append("Link must be a valid url")
        
        date_expires = self.request.get("date_expires")
        if date_expires != "":
            date_expires = datetime.strptime(date_expires, "%d/%m/%y").date()
        else:
            date_expires = None
            
        tags_raw = self.request.get("tags").strip(" ").split(" ")
        if len(tags_raw) == 1 and tags_raw[0] == "":
            errors.append("You must enter at least 1 tag")
        else:
            tags = [db.Category(x) for x in tags_raw]
        
        if len(errors) == 0:
            entry = Entry(link=link, 
                          tags = tags,
                          date_expires = date_expires)
            entry.put()
            self.redirect("?added=True")
        else:
            self.render_initial({"errors": errors, "args" : self.request.get})
        
        
        
    def render_initial(self, additional_values={}):
        result =  Entry.all().fetch(100)
        tags = [i for i in set([t for e in result for t in e.tags])]
        template_values = {"tags" : tags}
        template_values = dict(template_values.items() + additional_values.items())
        if "args" not in template_values:
            template_values["args"] = lambda x: None
        self.render_template("add.html", template_values)  
        
        
app = webapp2.WSGIApplication([('/new', Add)],
                              debug=True)

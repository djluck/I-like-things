import webapp2
from handlers.base import Base
from data.functions import *
from data.entities import Tag
from google.appengine.ext import db
from datetime import datetime
import urlparse
from google.appengine.api import users

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
        elif len(urlparse.urlparse(link)[1]) == 0:
            errors.append("Link must be a valid url")
        
        date_expires = self.request.get("date_expires")
        if date_expires != "":
            date_expires = datetime.strptime(date_expires, "%d/%m/%y").date()
        else:
            date_expires = None
            
        tags = self.request.get("tags").strip(" ").split(",")
        if len(tags) == 1 and tags[0] == "":
            errors.append("You must enter at least 1 tag")
        
        if len(errors) == 0:
            new_entry(link, tags, date_expires)
            self.redirect("?added=True")
        else:
            self.render_initial({"errors": errors, "args" : self.request.get})
        
        
        
    def render_initial(self, additional_values={}):
        template_values = {"tags" : [t.value for t in get_all_tags()]}
        template_values = dict(template_values.items() + additional_values.items())
        self.render_template("add.html", template_values)  
        
        
app = webapp2.WSGIApplication([('/new', Add)],
                              debug=True)

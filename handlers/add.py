import webapp2
from handlers.base import Base
from data.functions import *
from data.entities import Tag
from google.appengine.ext import db
from datetime import datetime
import urlparse
from google.appengine.api import users
import json

class Add(Base):
    def get(self):
        addedB = "added" in self.request.GET
        self.render_initial(added=addedB)
        
        
    def post(self):
        context = dict([(key, {"value": val}) for key, val in self.request.POST.items()]) #populate context with id's + values
        
        link = self.request.get("link").strip(" ")
        if len(link) > 0 and link[0:4] != "http":
            link = "http://" + link
        if len(link) == 0:
            context["link"]["error_msg"] = "Link must not be empty"
        elif len(urlparse.urlparse(link)[1]) == 0:
            context["link"]["error_msg"] = "Link must be a valid url"
        
        date_expires = self.request.get("date_expires")
        if date_expires != "":
            try:
                date_expires = datetime.strptime(date_expires, "%d/%m/%y").date()
            except:
                context["date_expires"]["error_msg"] = "Date must be in the dd/mm/yy format"
                date_expires = None
        else:
            date_expires = None
            
        tags = self.request.get("tags").strip(" ").split(" ")
        if len(tags) == 1 and tags[0] == "":
            context["tags"]["error_msg"] = "You must enter at least 1 tag"
        
        if "error_msg" not in context["link"] and "error_msg" not in context["tags"] and "error_msg" not in context["tags"]: #TODO: improve so we can have a attribute named 'has_errors'
            new_entry(link, tags, date_expires)
            self.redirect("?added=true")
        else:
            self.render_initial(context=context)
        
        
        
    def render_initial(self, **template_values):
        if "context" not in template_values:
            template_values["context"] = {}
            template_values["context"]["tags"] = {}
        template_values["context"]["tags"]["tags"] = json.dumps([t.value for t in get_all_tags()])
        self.render_template("add.html", template_values)  
        
        
app = webapp2.WSGIApplication([('/new', Add)],
                              debug=True)

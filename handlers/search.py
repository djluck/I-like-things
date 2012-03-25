import webapp2
from handlers.base import Base
from data.functions import *
from data.entities import Tag

class Search(Base):
    def get(self):
        search_on_tags = self.request.get("tags").rstrip(" ").split(" ")
        template_values = {"search_results" : search_by_tags(search_on_tags)} 
        self.render_template("search_results.html",  template_values)
        
app = webapp2.WSGIApplication([('/search', Search)],
                              debug=True)

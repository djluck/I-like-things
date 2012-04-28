import webapp2
import jinja2
import os
import json
from datetime import datetime, timedelta

class Base(webapp2.RequestHandler):
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../Templates/")) 

    def render_template(self, name, values):
        self.response.headers['Content-Type'] = 'text/html'
        template = self.jinja_env.get_template(name)
        self.response.out.write(template.render(values))
        
    def timesince(d):
        delta = datetime.now() - d
        values = None
        if delta.days > 0:
            values = (delta.days, "days")
        else:
            hours = delta.seconds / 3600
            minutes = delta.seconds / 60
            if hours > 0:
                values = (hours, "hours")
            elif minutes > 0:
                values = (minutes, "minutes")
            else:
                values = (delta.seconds, "seconds")
        return "%i %s ago" % values


    jinja_env.filters['timesince'] = timesince
    jinja_env.filters['json'] = json.dumps
import webapp2
import jinja2
import os



class Base(webapp2.RequestHandler):
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../Templates/")) 
  
    def render_template(self, name, values):
        self.response.headers['Content-Type'] = 'text/html'
        template = self.jinja_env.get_template(name)
        self.response.out.write(template.render(values))
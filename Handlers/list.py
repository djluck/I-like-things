import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../templates/"))

class List(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_environment.get_template('list.html')
        template_values = {"myname":"JAMES"}
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/.*', List)],
                              debug=True)
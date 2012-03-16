import webapp2

class Add(webapp2.RequestHandler):
      def get(self):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('ADD')

app = webapp2.WSGIApplication([('/new', Add)],
                              debug=True)
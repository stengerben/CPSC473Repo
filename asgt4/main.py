import webapp2

import cookies

cookies.SECRET = 's00p3rs33kr1t'

class MainHandler(webapp2.RequestHandler):
    def get(self):
        count = cookies.get(self.request, 'count', default='0')
        count = int(count) + 1
        cookies.set(self.response, 'count', count)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('%d\n' % count)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

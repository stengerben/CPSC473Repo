#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

class Greeting(db.Model):
    """Models an individual Guestbook entry"""
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

def guestbook_key(guestbook_name=None):
    """Constructs a Datastore key for Guestbook entity with guestbook_name."""
    return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.out.write('<html><body>')
            guestbook_name=self.request.get('guestbook_name')

            greetings = db.GqlQuery("SELECT * "
                                    "FROM Greeting "
                                    "WHERE ANCESTOR IS :1 "
                                    "ORDER BY date DESC LIMIT 10",
                                    guestbook_key(guestbook_name))

            for greeting in greetings:
                greetings.author = user.nickname()
                if greetings.author:
                    self.response.out.write(
                            '<b>%s</b> wrote:' % greetings.author)

                self.response.out.write('<blockquote>%s</blockquote>' %
                                        cgi.escape(greeting.content))

            self.response.out.write("""
                <form action="/sign?%s" method="post">
                    <div><textarea name="content" rows="3" cols="60"></textarea></div>
                    <div><input type="submit" value="Sign Guestbook"></div>
                </form>
                    <hr>
                    <form>Guestbook name: <input value="%s" name="guestbook_name">
                    <input type="submit" value="switch"></form>
                </body>
                </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                              cgi.escape(guestbook_name)))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))



app = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', Guestbook)],
                              debug=True)

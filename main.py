import os
import webapp2

from google.appengine.ext import ndb

class Trace(ndb.Model):
    prod = ndb.StringProperty()
    ver = ndb.StringProperty()
    guid = ndb.StringProperty()
    trace = ndb.BlobProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class UploadPage(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('REQUEST_LOG_ID=' +
                            (os.environ.get('REQUEST_LOG_ID')) + '\n')
    guestbook_name = self.request.get('name')
    self.response.write("Guestbook name: " + guestbook_name + '\n')
    #self.response.write(self.request.get('img'))
    trace_key = ndb.Key('Guestbook', 'default_guestbook')

    trace_object = Trace(parent=trace_key)
    trace_binary = self.request.get('trace')
    trace_object.trace = trace_binary
    trace_object.put()

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("""
          <form action="/upload" enctype="multipart/form-data" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="file" name="img"/></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
          <hr>
        </body>
      </html>""")

app = webapp2.WSGIApplication([('/', MainPage), ('/upload', UploadPage)])

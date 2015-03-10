import os
import webapp2

import cloudstorage as gcs

from google.appengine.api import app_identity

my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)


# class Trace(ndb.Model):
#     prod = ndb.StringProperty()
#     ver = ndb.StringProperty()
#     guid = ndb.StringProperty()
#     trace = ndb.BlobProperty()
#     date = ndb.DateTimeProperty(auto_now_add=True)

class UploadPage(webapp2.RequestHandler):
  def post(self):
    trace_guid = self.request.get('guid')

    # trace_object = Trace(parent=ndb.Key('Trace', trace_guid or "default_guid"))
    # trace_object.guid = trace_guid
    # trace_object.trace = self.request.get('trace')
    # trace_object.prod = self.request.get('prod')
    # trace_object.ver = self.request.get('ver')
    # trace_object.put()

    bucket_name = '/' + app_identity.get_default_gcs_bucket_name() + '/' + (trace_guid or 'default_guid')
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(bucket_name,
                        'w',
                        content_type='text/plain',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    gcs_file.write(self.request.get('trace'))
    gcs_file.close()

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("""
          <form action="/upload" enctype="multipart/form-data" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="file" name="trace"/></div>
            <div><input type="submit" value="Upload thingy"></div>
          </form>
          <hr>
        </body>
      </html>""")

app = webapp2.WSGIApplication([('/', MainPage), ('/upload', UploadPage)])

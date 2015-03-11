import os
import webapp2
import uuid

import cloudstorage as gcs
from google.appengine.ext import ndb
from google.appengine.api import app_identity

my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)

class UnprocessedTrace(ndb.Model):
    prod = ndb.StringProperty()
    ver = ndb.StringProperty()
    bucket_name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class UploadPage(webapp2.RequestHandler):
  def post(self):
    trace_uuid = str(uuid.uuid4())
    bucket_name = '/' + app_identity.get_default_gcs_bucket_name() + '/' + trace_uuid
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(bucket_name,
                        'w',
                        content_type='application/octet-stream',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    gcs_file.write(self.request.get('trace'))
    gcs_file.close()

    trace_object = UnprocessedTrace()
    trace_object.bucket_name = bucket_name
    trace_object.prod = self.request.get('prod')
    trace_object.ver = self.request.get('ver')
    trace_object.put()

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("""
          <form action="/upload" enctype="multipart/form-data" method="post">
            <div><input type="file" name="trace"/></div>
            <div><input type="submit" value="Upload"></div>
          </form>
          <hr>
        </body>
      </html>""")

app = webapp2.WSGIApplication([('/', MainPage), ('/upload', UploadPage)])

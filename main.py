import os
import webapp2
import uuid

import cloudstorage as gcs

from google.appengine.api import app_identity

my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)


class UploadPage(webapp2.RequestHandler):
  def post(self):
    bucket_name = '/' + app_identity.get_default_gcs_bucket_name() + '/' + str(uuid.uuid4())
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(bucket_name,
                        'w',
                        content_type='application/octet-stream',
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

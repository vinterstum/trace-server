from google.appengine.ext import ndb

class UnprocessedTrace(ndb.Model):
    prod = ndb.StringProperty()
    ver = ndb.StringProperty()
    bucket_name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

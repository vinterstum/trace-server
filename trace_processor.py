from google.appengine.ext import ndb

def touch(entity):
    """
    Update the entities timestamp.
    """
    entity.put()

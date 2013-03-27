#!/usr/bin/env python
from google.appengine.ext import db



################################################################################################################################################    
########################################################## DATABASE ############################################################################
################################################################################################################################################
class Users(db.Model):
    user = db.StringProperty(required = True)
    password = db.TextProperty(required=True)
    active = db.BooleanProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    
class Posts(db.Model):
    user = db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    introduction = db.TextProperty(required = True)
    content = db.TextProperty(required = True)
    link = db.StringProperty(required = False)
    

    
# Datastore index for user
def Users_key(username=None):
    """ Constructs a datastore key for a Users entity with username"""
    return db.key.from_path("user", username or 'default_user')
    
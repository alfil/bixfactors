#!/usr/bin/env python
from google.appengine.ext import db


################################################################################################################################################    
########################################################## FUNCTIONS ###########################################################################
################################################################################################################################################
"""
Check if a record already exists in the database
"""
def exist_in_db(table, values):
    str_sql = 'SELECT * FROM %s ' % table
    if len(values) == 1:
        str_sql += "WHERE %s = :1" % values.keys()[0]
        q = db.GqlQuery(str_sql, values[values.keys()[0]])
    elif len(values) == 2:
        str_sql += "WHERE %s = :1 AND %s = :2" % (values.keys()[0], values.keys()[1])
        q = db.GqlQuery(str_sql, values[values.keys()[0]], values[values.keys()[1]])
    
    
    
#    q = db.GqlQuery("SELECT * FROM %s WHERE %s = :1" % (table, field), value)
    for record in q:
        return True
    else:
        return False
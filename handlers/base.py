
import webapp2
from google.appengine.ext.webapp import template
import os
import logging

import fix_path




"""
Class that contains basic functions used for all handler classes, which will be inherited by them
"""
class BaseHandler(webapp2.RequestHandler):
    
    def __init__(self, request, response):
        self.initialize(request, response)
    
    def render_response(self, _template, template_values):
        # It gets the templates path from the fix_path module
        path = os.path.join(fix_path.templates_path, _template)
        self.response.out.write(template.render(path, template_values))
#!/usr/bin/env python


from handlers import *




# URL mapping
route_list = [
              ('/', MainHandler),
              ('/signin', SigninHandler),
              ('/signup', SignupHandler),
              ('/backindex', BackindexHandler),
              ('/backpost', BackpostHandler),
              ('/post', PostHandler)
              ]

import logging

# Project modules
from base import BaseHandler
from database_definition import *
from tools import *


# Mail
from google.appengine.api import mail










################################################################################################################################################    
########################################################## HOME PAGE ###########################################################################
################################################################################################################################################
class MainHandler(BaseHandler):
    def get(self):
        # Get all values in Posts
        q = db.GqlQuery("SELECT * FROM Posts")
        
        # Keys generation for the edition
        list_posts=[]
        for post in q:
            list_posts.append({'title': post.title, 'content': post.content, 'introduction': post.introduction,
                               'key': post.key()})
        
        ##### Template calling page index.html#####
        template_values = {'posts': list_posts}
        self.render_response('index.html', template_values)
        

            
################################################################################################################################################    
########################################################## SIGNIN PAGE #########################################################################
################################################################################################################################################
class SigninHandler(BaseHandler):
    
    def get(self): 
        ##### Template calling page signin.html#####
        template_values = {}
        self.render_response('signin.html', template_values)
        
    def post(self):
        
        ### Look for the record in the database to verify username/password
        entered_username = self.request.get("username")
        entered_password = self.request.get("password")
        error_username = ""
        error_password = ""
        try:
            q = db.GqlQuery("SELECT * FROM Users WHERE user = :1 ", entered_username)
            user = q.get()
            logging.info(user.user)
            
            if user.user:
                # Check of password
                if not valid_pw(entered_username, entered_password, user.password):
                        #Password is not correct
                        error_password = "La password no es correcta"
                # Check if it is active
                if not user.active:
                    error_username = "Usuario pendiente de aprobar"
                else:
                    # We hash the username for avoiding cheating
                    hash_username = hash_cookie(entered_username)
                    # It stores the username in a cookie
                    self.response.headers.add_header('Set-Cookie', str('username=%s' % hash_username))
                    # It redirects to the signed page
                    self.redirect ('/backindex')
                
                    
#                    self.request.cookies.get('name_cookie')
#                    self.response.headers.add_header('Set-Cookie', 'name=whatever')
                    

                    
            # It does not have found a user in the database        
            else:
                #User does not exist
                error_username = "Este usuario no existe"
                     
        except Exception as error:
            logging.error("Error while getting data from Users: " + str(error))
            error_username = "Error when getting the data"
        
        #If it has not been redirected there must have been an error, so we show it        
        ##### Template calling page signin.html#####
        template_values = {'username': entered_username, 'error_username': error_username, 'error_password': error_password}
        self.render_response('signin.html', template_values)
                
################################################################################################################################################    
########################################################## SIGNUP PAGE #########################################################################
################################################################################################################################################
class SignupHandler(BaseHandler):
    def get(self):
        ##### Template calling page signup.html#####
        template_values = {'username': '', 'error_username': '', 'error_password': '', 'error_verify': '', 'email': '', 'error_email': ''}
        self.render_response('signup.html', template_values)
        
    def post(self):
        # Get all the entered data
        entered_username = self.request.get("username")
        entered_password = self.request.get("password")
        entered_verify = self.request.get("verify")
        entered_email = self.request.get("email")
        # Validation of entered data
        valid_username = verify_username(entered_username)
        existing_username = check_existing_username(entered_username) 
        valid_password = verify_password(entered_password)
        valid_verify = verify_verify(entered_password, entered_verify)
        valid_email = verify_email(entered_email)
        # Check if data is ok
        if valid_username and valid_password and valid_verify and (valid_email or entered_email == "") and not existing_username:
            
            # Check if username already exists in the database
            
            
            # Hass the password
            hashed_password = make_pw_hash(entered_username, entered_password)
            a = Users(user=entered_username, password=hashed_password, active=False)
            a.put()
            # Call of welcome page
            ##### Template calling page signup.html#####
            template_values = {}
            self.render_response('index.html', template_values)
            
        else:
            # Test of each of the entered values
            username = ''
            error_username = ''
            error_password = ''
            error_verify = ''
            email = ''
            error_email = ''
            if valid_username == None:
                # I keep the entered value
                username = entered_username
                error_username = "That's not a valid username."
            if valid_password == None:
                # I don't keep the entered value and raise an error
                error_password = "That's not a valid password."
            if valid_verify == False:
                # I don't keep the entered value and raise an error
                error_verify = "Your passwords didn't match."
            if valid_email == None and entered_email != "":
                # I keep the entered value and raise an error
                email = entered_email
                error_email = "That's not a valid email."
            if existing_username == True:
                username = entered_username
                error_username = "This username already exist. Please, choose a new one."
            
            ##### Template calling page signup.html#####
            template_values = {'username': entered_username, 'error_username': error_username, 'error_password': error_password, 
                               'error_verify': error_verify, 'email': email, 'error_email': error_email}
            self.render_response('signup.html', template_values)
            
################################################################################################################################################    
########################################################## BACK INDEX ###########################################################################
################################################################################################################################################
class BackindexHandler(BaseHandler):
    def get(self):
        
        # Get all values in Posts
        q = db.GqlQuery("SELECT * FROM Posts")
        
        # Keys generation for the edition
        list_posts=[]
        for post in q:
            list_posts.append({'title': post.title, 'content': post.content, 'introduction': post.introduction,
                               'key': post.key()})
            
        ##### Template calling page index.html#####
        template_values = {'posts': list_posts}
        self.render_response('backindex.html', template_values)
        
    def post(self):
        # Nueva entrada
        self.redirect('/backpost')
        
################################################################################################################################################    
########################################################## BACK POST ###########################################################################
################################################################################################################################################
class BackpostHandler(BaseHandler):
    def get(self):
        
        #### Get tradeID ###
        postID = self.request.get("post")
        
        title=""
        content=""
        introduction=""
        if postID:
            #### Get values of the chosen post ####
            post=db.get(postID)
                   
            title = post.title
            content = post.content
            introduction = post.introduction
            
        
        
        
        ##### Template calling page index.html#####
        template_values = {'title': title, 'content': content, 'introduction': introduction}
        self.render_response('backpost.html', template_values)
        
    def post(self):
        
        # Case it cancels: It goes back to backindex
        if 'cancel' in self.request.POST:
            self.redirect('/backindex')
        
        # Case it saves    
        elif 'save' in self.request.POST:
            
            #### Get tradeID ###
            postID = self.request.get("post")
            logging.info('THE POST ID: ' + str(postID))
            
            # Variables initialization
            error_title = ""
            error_content = ""
            error_introduction = ""
            
            # We get all the entered data
            entered_title = self.request.get("title")
            entered_content = self.request.get("content")
            entered_introduction = self.request.get("introduction")
            logging.info(entered_title)
            logging.info(entered_content)
            logging.info(entered_introduction)
            
            
            # We check all data is ok
            valid_title = verify_title(entered_title)
            valid_content = verify_content(entered_content)
            valid_introduction = verify_introduction(entered_introduction)
            
            # If all fields ok, we save
            if valid_title and valid_content and valid_introduction:
                logging.info('Intenta grabar')
                try:
                    # If it is new
                    if not postID:
                        username = self.request.cookies.get('username').split('|')[0]
                        a=Posts(user=username, title=valid_title, content=valid_content, introduction=valid_introduction)
                        a.put()
                    # If we are editing
                    else:
                        post = db.get(postID)
                        post.title = valid_title
                        post.content = valid_content
                        post.introduction = valid_introduction
                        post.put()
                        
                        
                        
                    self.redirect('/backindex')
                    
                    
                except Exception as error:
                    logging.info('ERROR:' + str(error))
                
            else:
                logging.info('No intenta grabar')
                if not valid_title:
                    logging.info('valid_title: ' + str(valid_title))
                    error_title = "Campo obligatorio"
                elif not valid_content:
                    error_content = "Campo obligatorio"
                elif not valid_introduction:
                    error_introduction = "Campo obligatorio"
                    
                template_values = {'title': entered_title, 'content': entered_content, 'introduction': entered_introduction, 
                                   'error_title': error_title, 'error_content': error_content, 'error_introduction': error_introduction}
                self.render_response('backpost.html', template_values)
            
            
            
    ################################################################################################################################################    
########################################################## POST ###########################################################################
################################################################################################################################################
class PostHandler(BaseHandler):
    def get(self):
        
        #### Get tradeID ###
        postID = self.request.get("post")
    
        if postID:
            #### Get values of the chosen post ####
            post=db.get(postID)
                   
            title = post.title
            content = post.content
            introduction = post.introduction
            
        
        
        
        ##### Template calling page index.html#####
        template_values = {'title': title, 'content': content, 'introduction': introduction}
        self.render_response('post.html', template_values)
        
    def post(self):
        
        # Case it cancels: It goes back to backindex
        if 'back' in self.request.POST:
            self.redirect('/')
        
        
         
            
            
            
            
            
            
            
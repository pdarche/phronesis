import tornado.web
import tornado.auth
import mixins
import json
import datetime
import time

#mongo and models
from mongoengine import *
import models

#python mongo hooks
from pymongo import MongoClient
import bson

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("username")

class MainHandler(BaseHandler): 
	def get(self):
		self.render( "index.html" )

class SignUpHandler(tornado.web.RequestHandler):
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		
		#if the username isn't already taken, create new user object 
		if len( models.User.objects(username=username) ) == 0:
			newuser = models.User(
				date = datetime.datetime.fromtimestamp(time.time()),
				username = username,
				password = password,
				offset_from_utc_millis = None,
				date_of_birth = None,
				fitbit_user_info = None,
				foursquare_user_info = None,
				flickr_user_info = None,
				facebook_user_info = None,
				khanacademy_user_info = None,
				twitter_user_info = None,
				google_user_info = None
			)

			if newuser.save():
				response = "all signed up!\n"
			else:
				response = "snap, somethin got f'd up\n"		
		else:
			response = "that username is not available!\n"

		self.write( response )


class LoginHandler(tornado.web.RequestHandler):
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')

		user = models.User.objects(username=username)

		if len( user ) == 0 or username == None:
			response = "Der, we don't have a user with that username\n"
		elif password != user[0].password:
			response = "Sorry brah, password mismatch\n"
		else:
			self.set_secure_cookie("username", username)
			response = "logged in\n"

		self.write( response )

	def get(self):
		# username = self.get_secure_cookie("user")
		# self.render('login.html', response=username)
		self.write( "redirect to login")


class UserInfoHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, input):
		print "input is %s" % input
		if input == self.current_user:
			
			user = models.User.objects(username=input)
			# self.render('test.html', user=response)
			response = { 				
				# "date" : user[0].date
				"username" : user[0].username,
				"offset_from_utc_millis" : user[0].offset_from_utc_millis,
				"time_zone" : user[0].time_zone,
				# "date_of_birth" : user[0].date_of_birth,
				"fitibt" : user[0].fitbit_user_info,
				"foursquare_user_info" : user[0].foursquare_user_info,
				"flickr_user_info" : user[0].flickr_user_info,
				"facebook_user_info" : user[0].facebook_user_info,
				"khanacademy_user_info" : user[0].khanacademy_user_info,
				"twitter_user_info" : user[0].twitter_user_info 
			}

			print "signup date is %r" % user[0].date

			self.write( json.dumps(response) )
		else:
			response
			self.render('test.html', user=input)


class TwitterHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin): 
	@tornado.web.asynchronous
	def get(self):
		oAuthToken = self.get_secure_cookie('tw_oauth_token')
		oAuthSecret = self.get_secure_cookie('tw_oauth_secret')
		userID = self.get_secure_cookie('tw_user_id')

		if self.get_argument('oauth_token', None):
			self.get_authenticated_user(self.async_callback(self._twitter_on_auth))
			return

		elif oAuthToken and oAuthSecret:
				accessToken = {
					'key': 		oAuthToken,
					'secret':	oAuthSecret
				}

				self.twitter_request('/users/show',
					access_token =  accessToken,
					user_id =		userID,
					callback = 		self.async_callback(self._twitter_on_user)
				)
				return

		self.authorize_redirect()

	def _twitter_on_auth(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Twitter authentication failed')

		self.set_secure_cookie('tw_user_id', str(user['id']))
		self.set_secure_cookie('tw_oauth_token', user['access_token']['key'])
		self.set_secure_cookie('tw_oauth_secret', user['access_token']['secret'])

		self.redirect('/twitter')

	def _twitter_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

		self.render('test.html', user=json.dumps(user))



class FacebookHandler(tornado.web.RequestHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.asynchronous
	def get(self):
		userId = self.get_secure_cookie('fb_user_id')

		if self.get_argument('code', None):
			print "getting authenticated user"
			self.get_authenticated_user(
				redirect_uri 	= 'http://localhost:8000/facebook',
				client_id 		= self.settings['facebook_api_key'],
				client_secret 	= self.settings['facebook_secret'],
				code 			= self.get_argument('code'),
				callback 		= self.async_callback(self._on_facebook_login)
			)
			return

		elif self.get_secure_cookie('fb_access_token'):
			self.write('logged into the facebook')

		self.authorize_redirect(
			redirect_uri 	= 'http://localhost:8000/facebook',
			client_id 		= self.settings['facebook_api_key'],
			extra_params	= { 'scope' : 'read_stream, publish_stream' }
		)

	def _on_facebook_login(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Facebook authentication failed')

		self.set_secure_cookie('fb_user_id', str(user['id']))
		self.set_secure_cookie('fb_user_name', str(user['name']))
		self.set_secure_cookie('fb_access_token', str(user['access_token']))
		self.render('test.html', user=json.dumps(user))



class FitbitHandler(tornado.web.RequestHandler, mixins.FitbitMixin): 
	@tornado.web.asynchronous
	def get(self):
		oAuthToken = self.get_secure_cookie('fitbit_oauth_token')
		oAuthSecret = self.get_secure_cookie('fitbit_oauth_secret')
		userID = self.get_secure_cookie('fitbit_user_id')

		if self.get_argument('oauth_token', None):			
			self.get_authenticated_user(self.async_callback(self._fitbit_on_auth))
			return

		elif oAuthToken and oAuthSecret:
				accessToken = {
					'key': 		oAuthToken,
					'secret':	oAuthSecret
				}

				self.fitbit_request('/users/show',
					access_token =  accessToken,
					user_id =		userID,
					callback = 		self.async_callback(self._fitbit_on_user)
				)
				return

		self.authorize_redirect()

	def _fitbit_on_auth(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Fitbit authentication failed')

		self.set_secure_cookie('fitbit_user_id', str(user['user']['encodedId']))
		self.set_secure_cookie('fitbit_oauth_token', user['access_token']['key'])
		self.set_secure_cookie('fitbit_oauth_secret', user['access_token']['secret'])

		self.render('test.html', user=json.dumps(user) )
		# self.write( json.dumps(user) )

	def _fitbit_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

		self.render('test.html', user=user)



class ZeoHandler(tornado.web.RequestHandler, mixins.ZeoMixin): 
	@tornado.web.asynchronous
	def get(self):
		oAuthToken = self.get_secure_cookie('zeo_oauth_token')
		oAuthSecret = self.get_secure_cookie('zeo_oauth_secret')
		userID = self.get_secure_cookie('zeo_user_id')

		if self.get_argument('oauth_token', None):	
			self.get_authenticated_user(self.async_callback(self._zeo_on_auth))
			return

		elif oAuthToken and oAuthSecret:
				accessToken = {
					'key': 		oAuthToken,
					'secret':	oAuthSecret
				}

				self.zeo_request('/users/show',
					access_token =  accessToken,
					user_id =		userID,
					callback = 		self.async_callback(self._fitbit_on_user)
				)
				return

		self.authorize_redirect('http://localhost:8000/zeo')

	def _zeo_on_auth(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Zeo authentication failed')

		self.set_secure_cookie('zeo_user_id', str(user['user']['encodedId']))
		self.set_secure_cookie('zeo_oauth_token', user['access_token']['key'])
		self.set_secure_cookie('zeo_oauth_secret', user['access_token']['secret'])

		self.render('test.html', user=json.dumps(user))

	def _zeo_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

		self.render('test.html', user=json.dumps(user))



class FoursquareHandler(tornado.web.RequestHandler, mixins.FoursquareMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri='http://localhost:8000/foursquare',
                client_id=self.settings["foursquare_client_id"],
                client_secret=self.settings["foursquare_client_secret"],
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_login)
            )
            return

        self.authorize_redirect(
			redirect_uri='http://localhost:8000/foursquare',
            client_id=self.settings["foursquare_api_key"]
        )

    def _on_login(self, user):
        # Do something interesting with user here. See: user["access_token"]
        self.render('test.html', user=json.dumps(user))
        


class GoogleHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
	@tornado.web.asynchronous
	def get(self):
		if self.get_argument("openid.mode", None):
		   self.get_authenticated_user(self.async_callback(self._on_auth))
		   return
		self.authenticate_redirect()

	def _on_auth(self, user):
		if not user:
		    raise tornado.web.HTTPError(500, "Google auth failed")
		self.render('test.html', user=json.dumps(user))
        # Save the user with, e.g., set_secure_cookie()


class FlickrHandler(tornado.web.RequestHandler, mixins.FlickrMixin):
	@tornado.web.asynchronous
	def get(self):
		oAuthToken = self.get_secure_cookie('flickr_oauth_token')
		oAuthSecret = self.get_secure_cookie('flickr_oauth_secret')
		# userID = self.get_secure_cookie('flickr_user_id')

		if self.get_argument('oauth_token', None):			
			self.get_authenticated_user(self.async_callback(self._flickr_on_auth))
			return

		elif oAuthToken and oAuthSecret:
				accessToken = {
					'key': 		oAuthToken,
					'secret':	oAuthSecret
				}

				self.flickr_request('method=flickr.urls.getUserProfile',
					access_token =  accessToken,
					user_id =		userID,
					callback = 		self.async_callback(self._flickr_on_user)
				)
				return

		self.authorize_redirect('http://localhost:8000/flickr')

	def _flickr_on_auth(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Flickr authentication failed')

		# self.set_secure_cookie('fitbit_user_id', str(user['user']['encodedId']))
		# self.set_secure_cookie('fitbit_oauth_token', user['access_token']['key'])
		# self.set_secure_cookie('fitbit_oauth_secret', user['access_token']['secret'])

		self.render('test.html', user=json.dumps(user))

	def _flickr_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

		self.render('test.html', user=user)


class KhanAcademyHandler(tornado.web.RequestHandler, mixins.KhanAcademyMixin):
	@tornado.web.asynchronous
	def get(self):
		oAuthToken = self.get_secure_cookie('khanacademy_oauth_token')
		oAuthSecret = self.get_secure_cookie('khanacademy_oauth_secret')
		# userID = self.get_secure_cookie('flickr_user_id')

		if self.get_argument('oauth_token', None):			
			self.get_authenticated_khanacademy_user(self.async_callback(self._khanacademy_on_auth))
			return

		elif oAuthToken and oAuthSecret:
				accessToken = {
					'key': 		oAuthToken,
					'secret':	oAuthSecret
				}

				self.khanacademy_request('/user',
					access_token =  accessToken,
					user_id =		userID,
					callback = 		self.async_callback(self._khanacademy_on_user)
				)
				return

		self.khanacademy_authorize_redirect('http://localhost:8000/khanacademy')  # Khan Academy requires a callback url

	def _khanacademy_on_auth(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Khan Academy authentication failed')

		# self.set_secure_cookie('fitbit_user_id', str(user['user']['encodedId']))
		# self.set_secure_cookie('fitbit_oauth_token', user['access_token']['key'])
		# self.set_secure_cookie('fitbit_oauth_secret', user['access_token']['secret'])

		self.render('test.html', user=json.dumps(user))

	def _khanacademy_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

		self.render('test.html', user=user)

class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_all_cookies()
		self.write('loggged out, yo\n')

class RemoveUserHandler(tornado.web.RequestHandler):
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		
		user = models.User.objects(username=username, password=password)

		user[0].delete(safe=True)
		self.write("user deleted\n")



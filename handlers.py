import tornado.web
import tornado.auth
import mixins
import json
import simplejson
import datetime
import time
from utilities import *

#mongo and models
from mongoengine import *
import models

#python mongo hooks
from pymongo import MongoClient
import bson

from bson import json_util

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
				date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
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
			
			response = json.dumps(user[0], default=encode_model)			

			print "fb user info %r" % user[0].facebook_user_info
			print "fb user info %r" % user[0].id

			self.write( response )
		else:
			response
			self.render('test.html', user=input)


class TwitterConnectHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin): 
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

		self.redirect('/twitter')

	def _twitter_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")


		tw = models.TwitterUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			twitter_default_profile_image = user["default_profile_image"],
			twitter_id = user["id"],
			twitter_verified = user["verified"],
			twitter_profile_image_url_https = user["profile_image_url_https"],
			twitter_id_str = user["id_str"],
			twitter_utc_offset = user["utc_offset"],
			twitter_location = user["location"],
			twitter_profile_image_url = user["profile_image_url"],
			twitter_geo_enabled = user["geo_enabled"],
			twitter_name = user["name"],
			twitter_lang = user["lang"],
			twitter_screen_name = user["screen_name"],
			twitter_url = user["url"],
			twitter_contributors_enabled = user["contributors_enabled"],
			twitter_time_zone = user["time_zone"],
			twitter_protected = user["protected"],
			twitter_default_profile = user["default_profile"],
			twitter_is_translator = user["is_translator"]
		)

		user_obj = models.User.objects(username=self.get_secure_cookie("username"))
		user_obj[0].update(set__twitter_user_info=tw)

		if user_obj[0].save():
			response = "saved"
			print "saved"
		else:
			response = "something was f'd up"
			print "not saved"

		self.write(response)
		self.finish()

		self.render('test.html', user=json.dumps(user))



class FacebookConnectHandler(tornado.web.RequestHandler, tornado.auth.FacebookGraphMixin):
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
		
		fb = models.FacebookUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			facebook_picture = user["picture"]["data"]["url"],
			facebook_first_name = user["first_name"],
			facebook_last_name = user["last_name"],
			facebook_name = user["name"],
			facebook_locale = user["locale"],
			facebook_access_token = user["access_token"],
			facebook_link = user["link"],
			facebook_id = user["id"]
		)

		user_obj = models.User.objects(username=self.get_secure_cookie("username"))
		user_obj[0].update(set__facebook_user_info=fb)

		if user_obj[0].save():
			response = "saved"
			print "saved"
		else:
			response = "something was f'd up"
			print "not saved"

		self.write(response)
		self.finish()



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
					callback = 		self.async_callback(self._fitbit_on_auth)
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

		ftbt_access = models.FitbitAccessToken(
			key = user["access_token"]["key"],
			encoded_user_id = user["access_token"]["encoded_user_id"],
			secret = user["access_token"]["secret"]
		)

		ftbt = models.FitbitUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			fitbit_user_name = user["username"],
			fitbit_access_token = ftbt_access,
			fitbit_weight_unit = user["user"]["weightUnit"],
			fitbit_stride_length_walking = user["user"]["strideLengthWalking"],
			fitbit_display_name = user["user"]["displayName"],
			fitbit_foodsl_locale = user["user"]["foodsLocale"],
			fitbit_height_unit = user["user"]["heightUnit"],
			fitbit_locale = user["user"]["locale"],
			fitbit_gender = user["user"]["gender"],
			fitbit_member_since = user["user"]["memberSince"],
			fitbit_offset_from_utc_millis = user["user"]["offsetFromUTCMillis"],
			fitbit_encoded_id = user["user"]["encodedId"],
			fitbit_avatar = user["user"]["avatar"],
			fitbit_water_unit = user["user"]["waterUnit"],
			fitbit_distance_unit = user["user"]["distanceUnit"],
			fitbit_glucose_unit = user["user"]["glucoseUnit"],
			fitbit_full_name = user["user"]["fullName"],
			fitbit_nickname = user["user"]["nickname"],
			fitbit_stride_length_running = user["user"]["strideLengthRunning"]
		)

		user_obj = models.User.objects(username=self.get_secure_cookie("username"))
		user_obj[0].update(set__fitbit_user_info=ftbt)

		if user_obj[0].save():
			response = "saved"
			print "saved"
		else:
			response = "something was f'd up"
			print "not saved"

		self.write(response)
		self.finish()

	def _fitbit_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")



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
        
		fs = models.FoursquareUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			foursquare_last_name = user["last_name"],
			foursquare_first_name = user["first_name"],
			foursquare_access_token = user["access_token"],
			foursquare_user_photo = user["response"]["user"]["photo"],
			foursquare_pings = user["response"]["user"]["pings"],
			foursquare_home_city = user["response"]["user"]["homeCity"],
			foursquare_id = user["response"]["user"]["id"],
			foursquare_bio = user["response"]["user"]["bio"],
			foursquare_relationship = user["response"]["user"]["relationship"],
			foursquare_checkin_pings = user["response"]["user"]["checkinPings"]
		)

		user_obj = models.User.objects(username=self.get_secure_cookie("username"))
		user_obj[0].update(set__foursquare_user_info=fs)

		if user_obj[0].save():
			response = "saved"
			print "saved"
		else:
			response = "something was f'd up"
			print "not saved"

		self.write(response)
		self.finish()


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

		g = models.GoogleUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			google_first_name = user["first_name"],
			google_claimed_id = user["claimed_id"],
			google_name = user["name"],
			google_locale = user["locale"],
			google_last_name = user["last_name"],
			google_email = user["email"]
		)
		
		user_obj = models.User.objects(username=self.get_secure_cookie("username"))
		user_obj[0].update(set__google_user_info=g)

		if user_obj[0].save():
			response = "saved"
			print "saved"
		else:
			response = "something was f'd up"
			print "not saved"

		self.write(response)
		self.finish()

		# self.render('test.html', user=json.dumps(user))
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

		flkr_access = models.FlickrAccessToken(
			flickr_usernam = user["access_token"]["username"],
			flickr_secret = user["access_token"]["secret"],
			flickr_full_name = user["access_token"]["fullname"],
			flickr_key = user["access_token"]["key"],
			flickr_nsid = user["access_token"]["user_nsid"]
		)

		flkr = models.FlickrUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			flickr_access_token = flkr_access,
			flickr_stat = user["stat"],
			flickr_user_url = user["user"]["url"],
			flickr_nsid = user["user"]["nsid"]
		)

		user_obj = models.User.objects(username=self.get_secure_cookie("username"))
		user_obj[0].update(set__flickr_user_info=flkr)

		if user_obj[0].save():
			response = "saved"
			print "saved"
		else:
			response = "something was f'd up"
			print "not saved"

		self.write(response)
		self.finish()
		# self.render('test.html', user=json.dumps(user))

	def _flickr_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

		# self.render('test.html', user=user)


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

		ka_access = models.KhanAcademyAccessToken(
			khanacademy_secret = user["access_token"]["secret"],
			khanacademy_key = user["access_token"]["key"],
		)

		ka = models.KhanAcademyUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			khanacademy_has_notification = user["has_notification"],
			khanacademy_can_record_tutorial = user["can_record_tutorial"],
			khanacademy_is_demo = user["is_demo"],
			khanacademy_key_email = user["key_email"].encode('utf-8'),
			khanacademy_is_pre_phantom = user["is_pre_phantom"],
			khanacademy_developer = user["developer"],
			khanacademy_user_id = user["user_id"].encode('utf-8'),
			khanacademy_is_google_user = user["is_google_user"],
			khanacademy_profile_root = user["profile_root"].encode('utf-8'),
			khanacademy_has_email_subscription = user["has_email_subscription"],
			khanacademy_discussion_banned = user["discussion_banned"],
			khanacademy_is_phantom = user["is_phantom"],
			khanacademy_email = user["email"].encode('utf-8'),
			khanacademy_is_facebook_user = user["is_facebook_user"],
			khanacademy_is_midsignup_phantom = user["is_midsignup_phantom"],
			# khanacademy_auth_emails = auth_emails,
			khanacademy_last_modified_as_mapreduce_epoch = user["last_modified_as_mapreduce_epoch"],
			khanacademy_uservideocss_version = user["uservideocss_version"],
			khanacademy_nickname = user["nickname"].encode('utf-8'),
			# khanacademy_user_input_auth_emails = user["user_input_auth_emails"],
			khanacademy_kind = user["kind"].encode('utf-8'),
			khanacademy_is_moderator_or_developer = user["is_moderator_or_developer"],
			khanacademy_joined = user["joined"].encode('utf-8'),
			khanacademy_userprogresscache_version = user["userprogresscache_version"],
			khanacademy_gae_bingo_identity = user["gae_bingo_identity"].encode('utf-8')
		)

		user_obj = models.User.objects(username=self.get_secure_cookie("username"))
		user_obj[0].update(set__khanacademy_user_info=ka)

		if user_obj[0].save():
			response = "saved"
			print "saved"
		else:
			response = "something was f'd up"
			print "not saved"

		self.write(response)

		self.finish()

		# self.render('test.html', user=json.dumps(user))


	def _khanacademy_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

		# self.render('test.html', user=user)

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



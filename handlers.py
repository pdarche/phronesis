#!/usr/bin/env python
# -*- coding: utf8 -*- 
import tornado.web
import tornado.auth
import tornado.gen
import mixins.mixins as mixins 
import json
import simplejson
import datetime
import time
import zeoapi
from utilities import *
import os

import oauth2 
import urllib 
import urllib2

#mongo and models
from mongoengine import *
import models
import models.location as loc
import models.physact as physact
import models.sleep as sleep
import models.mypyramid as pyramid
import models.nutrition as nutrition
import models.healthy as healthy

#python mongo hooks
from pymongo import *
from pymongo import MongoClient
import bson

from bson import json_util
from bson import objectid

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("username")

class MainHandler(BaseHandler): 
	def get(self):
		username = self.get_secure_cookie('username')
		if username != None:
			self.render('index.html', username = username)
		else:
			self.render( "index.html", username = "" )

# class BSHandler(BaseHandler): 
# 	def post(self):
# 		# username = self.get_secure_cookie('username')
# 		user = models.userinfo.User.objects(username='pdarche')[0]
# 		adjectives = models.userinfo.UserAdjectives(
# 				first_priority = "healthy",
# 				first_priority_specific = "cardiovascular",
# 				second_priority = "sustainable",
# 				second_priority_specific = "carbon",
# 				third_priority = "educated",
# 				third_priority_specific = "mathematical",
# 			)

# 		user.update(set__adjectives=adjectives)


class SignUpHandler(tornado.web.RequestHandler):
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		
		#if the username isn't already taken, create new user object 
		if len( models.userinfo.User.objects(username=username) ) == 0:
			
			adjectives = models.userinfo.UserAdjectives(
				first_priority = None,
				first_priority_specifics = None,
				second_priority = None,
				second_priority_specifics = None,
				third_priority = None,
				third_priority_specifics = None,
			)

			newuser = models.userinfo.User(
				date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
				username = username,
				password = password,
				offset_from_utc_millis = None,
				date_of_birth = None,
				ftbt_user_info = None,
				foursquare_user_info = None,
				flickr_user_info = None,
				facebook_user_info = None,
				khanacademy_user_info = None,
				twitter_user_info = None,
				google_user_info = None,
				adjectives = adjectives
			)

			if newuser.save():
				response = "all signed up!\n"
			else:
				response = "snap, somethin got f'd up\n"		
		else:
			response = "that username is not available!\n"

		self.write(response)


class LoginHandler(tornado.web.RequestHandler):
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')

		user = models.userinfo.User.objects(username=username)

		if len( user ) == 0 or username == None:
			response = "Der, we don't have a user with that username\n"
		elif password != user[0].password:
			response = "Sorry brah, password mismatch\n"
		else:
			self.set_secure_cookie("username", username)
			response = "success"

		self.write(response)

	def get(self):
		# username = self.get_secure_cookie("user")
		# self.render('login.html', response=username)
		self.write( "redirect to login")


class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_all_cookies()
		self.redirect('/')


class UserInfoHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, input):
		print "input is %s" % input
		if input == self.current_user:
			
			user = models.userinfo.User.objects(username=input)
			
			response = json.dumps(user[0], default=encode_model)			

			print "fb user info %r" % user[0].facebook_user_info
			print "fb user info %r" % user[0].id

			self.write(response)
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
					'key': oAuthToken,
					'secret': oAuthSecret
				}

				self.twitter_request('/users/show',
					access_token = accessToken,
					user_id = userID,
					callback = self.async_callback(self._twitter_on_user)
				)
				return

		self.authorize_redirect()

	def _twitter_on_auth(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Twitter authentication failed')

		self.redirect('/v1/twitter')

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

		user_obj = models.userinfo.User.objects(username=self.get_secure_cookie("username"))
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
				redirect_uri = 'http://localhost:8000//v1/facebook',
				client_id = self.settings['facebook_api_key'],
				client_secret = self.settings['facebook_secret'],
				code = self.get_argument('code'),
				callback = self.async_callback(self._on_facebook_login)
			)
			return

		elif self.get_secure_cookie('fb_access_token'):
			self.write('logged into the facebook')

		self.authorize_redirect(
			redirect_uri = 'http://localhost:8000/v1/facebook',
			client_id = self.settings['facebook_api_key'],
			extra_params = { 'scope' : 'read_stream, publish_stream' }
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

		user_obj = models.userinfo.User.objects(username=self.get_secure_cookie("username"))
		user_obj[0].update(set__facebook_user_info=fb)

		if user_obj[0].save():
			response = "saved"
			print "saved"
		else:
			response = "something was f'd up"
			print "not saved"

		self.write(response)
		self.finish()



class FitbitConnectHandler(BaseHandler, mixins.FitbitMixin): 
	@tornado.web.authenticated
	@tornado.web.asynchronous
	def get(self):

		curr_user = models.userinfo.User.objects(username=self.get_secure_cookie("username"))[0]

		if self.get_argument('oauth_token', None):			
			self.get_authenticated_user(self.async_callback(self._fitbit_on_auth))
			return

		elif hasattr(curr_user["ftbt_user_info"], "ftbt_access_token"):
				oAuthToken = curr_user["ftbt_user_info"]["ftbt_access_token"]["key"]
				oAuthSecret = curr_user["ftbt_user_info"]["ftbt_access_token"]["secret"]
				userID = curr_user["ftbt_user_info"]["ftbt_access_token"]["encoded_user_id"]

				accessToken = {
					'key': 		oAuthToken,
					'secret':	oAuthSecret
				}

				self.fitbit_request('/user/-/activities/log/steps/date/today/7d',
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

		ftbt_access = models.userinfo.FitbitAccessToken(
			key = user["access_token"]["key"],
			encoded_user_id = user["access_token"]["encoded_user_id"],
			secret = user["access_token"]["secret"]
		)

		ftbt = models.userinfo.FitbitUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			fitbit_user_name = user["username"],
			ftbt_access_token = ftbt_access,
			ftbt_weight_unit = user["user"]["weightUnit"],
			ftbt_stride_length_walking = user["user"]["strideLengthWalking"],
			ftbt_display_name = user["user"]["displayName"],
			ftbt_foodsl_locale = user["user"]["foodsLocale"],
			ftbt_height_unit = user["user"]["heightUnit"],
			ftbt_locale = user["user"]["locale"],
			ftbt_gender = user["user"]["gender"],
			ftbt_member_since = user["user"]["memberSince"],
			ftbt_offset_from_utc_millis = user["user"]["offsetFromUTCMillis"],
			ftbt_encoded_id = user["user"]["encodedId"],
			ftbt_avatar = user["user"]["avatar"],
			ftbt_water_unit = user["user"]["waterUnit"],
			ftbt_distance_unit = user["user"]["distanceUnit"],
			ftbt_glucose_unit = user["user"]["glucoseUnit"],
			ftbt_full_name = user["user"]["fullName"],
			ftbt_nickname = user["user"]["nickname"],
			ftbt_stride_length_running = user["user"]["strideLengthRunning"]
		)

		user_obj = models.userinfo.User.objects(username=self.get_secure_cookie("username"))
		user_obj[0].update(set__ftbt_user_info=ftbt)

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

		self.write(json.dumps(user))
		self.finish()

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

	def _zeo_on_auth(self, *args):		
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Zeo authentication failed')

		# self.render('test.html', user=json.dumps(user))

	def _zeo_on_user(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, "Couldn't retrieve user information")

		self.render('test.html', user=json.dumps(user))


class ZeoBasicAuth(tornado.web.RequestHandler):
	@tornado.web.authenticated
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		user = models.userinfo.User.objects(username="pdarche")[0]

		zeo = models.userinfo.ZeoUserInfo(
			create_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			zeo_username = username,
			zeo_password = password
		)

		user.update(set__zeo_user_info=zeo)

		if user.save():
			response = "zeo added"
			print "user saved"
		else:
			response = "failure"
			print "user not saved"

		self.write(response)
		self.finish()

	@tornado.web.asynchronous
	def get(self):
		user = models.userinfo.User.objects(username=self.get_secure_cookie("username"))[0]
		zeo_username = user.zeo_user_info.zeo_username
		zeo_password = user.zeo_user_info.zeo_password
		api_key = '99B70750EA14609996C38F0B4618D934'

		z = zeoapi.Api()
		z.username = zeo_username
		z.password = zeo_password
		z.apikey = api_key
		z.referrer = "http://localhost:8000"

		data = z.getAllDatesWithSleepData()
		nights = []

		for d in data:
			date = '%s-%s-%s' % (d["year"], d["month"], d["day"])
			record = z.getSleepRecordForDate(date=date)
		 	
		 	for_date = models.zeo.ZeoDateTime(
		 		year = record["startDate"]["year"],
		 		month = record["startDate"]["month"],
		 		day = record["startDate"]["day"],
		 		hour = None,
		 		minute = None,
		 		second = None
		 	)

		 	bed_time = models.zeo.ZeoDateTime(
		 		year = record["bedTime"]["year"],
		 		month = record["bedTime"]["month"],
		 		day = record["bedTime"]["day"],
		 		hour = record["bedTime"]["hour"],
		 		minute = record["bedTime"]["hour"],
		 		second = record["bedTime"]["second"]
		 	)

		 	rise_time = models.zeo.ZeoDateTime(
		 		year = record["riseTime"]["year"],
		 		month = record["riseTime"]["month"],
		 		day = record["riseTime"]["day"],
		 		hour = record["riseTime"]["hour"],
		 		minute = record["riseTime"]["hour"],
		 		second = record["riseTime"]["second"]
		 	)

		 	sleep_graph_start = models.zeo.ZeoDateTime(
		 		year = record["sleepGraphStartTime"]["year"],
		 		month = record["sleepGraphStartTime"]["month"],
		 		day = record["sleepGraphStartTime"]["day"],
		 		hour = record["sleepGraphStartTime"]["hour"],
		 		minute = record["sleepGraphStartTime"]["hour"],
		 		second = record["sleepGraphStartTime"]["second"]
		 	)

			sleep_record = models.zeo.ZeoSleepRecord(
				phro_created_at = int(time.time()),
				username = self.get_secure_cookie("username"),
				start_date = for_date,
				awakenings = record["awakenings"],
				awakenings_zq_points = record["awakeningsZqPoints"],
				bed_time = bed_time,
				grouping = record["grouping"],
				morning_feel = record["morningFeel"],
				rise_time = rise_time,
				time_in_deep = record["timeInDeep"],
				time_in_deep_percentage = record["timeInDeepPercentage"],
				time_in_deep_zq_points = record["timeInDeepZqPoints"],
				time_in_light = record["timeInLight"],
				time_in_light_percentage = record["timeInLightPercentage"],
				time_in_rem = record["timeInRem"],
				time_in_rem_percentage = record["timeInRemPercentage"],
				time_in_rem_zq_points = record["timeInRemZqPoints"],
				time_in_wake = record["timeInWake"],
				time_in_wake_percentage = record["timeInWakePercentage"],
				time_in_wake_zq_points = record["timeInWakeZqPoints"],
				time_to_z = record["timeToZ"],
				total_z = record["totalZ"],
				totalz_z_zq_points = record["totalZZqPoints"],
				zq = record["zq"],
				alarm_reason = record["alarmReason"],
				alarm_ring_index = record["alarmRingIndex"],
				day_feel = record["dayFeel"],
				sleep_graph = record["sleepGraph"],
				sleep_graph_start_time = sleep_graph_start,
				sleep_stealer_score = record["sleepStealerScore"],
				wake_window_end_index = record["wakeWindowEndIndex"],
				wake_window_start_index = record["wakeWindowStartIndex"]
			)

			if sleep_record.save():
				response = "sleep record saved"
				print "sleep record saved"
			else:
				response = "sleep record didn't"
				response = "sleep record didn't save"

		self.write(response)
		self.finish()

	def _on_data(self, data):
		self.write( json.dumps( data ))
		self.finish()

class FoursquareHandler(tornado.web.RequestHandler, mixins.FoursquareMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri='http://localhost:8000/v1/foursquare',
                client_id=self.settings["foursquare_client_id"],
                client_secret=self.settings["foursquare_client_secret"],
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_login)
            )
            return

        self.authorize_redirect(
			redirect_uri='http://localhost:8000/v1/foursquare',
            client_id=self.settings["foursquare_api_key"]
        )

    def _on_login(self, user):
        # Do something interesting with user here. See: user["access_token"]
        
		fs = models.userinfo.FoursquareUserInfo(
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

		user_obj = models.userinfo.User.objects(username=self.get_secure_cookie("username"))
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

		g = models.userinfo.GoogleUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			google_first_name = user["first_name"],
			google_claimed_id = user["claimed_id"],
			google_name = user["name"],
			google_locale = user["locale"],
			google_last_name = user["last_name"],
			google_email = user["email"]
		)
		
		user_obj = models.userinfo.User.objects(username=self.get_secure_cookie("username"))
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
		print "is there a secret %r" % oAuthSecret

		if self.get_argument('oauth_token', None):			
			print "got request token"
			self.get_authenticated_user(self.async_callback(self._flickr_on_auth))
			return

		elif oAuthToken and oAuthSecret:
				print "got acces and secret"
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

		self.authorize_redirect('http://localhost:8000/v1/flickr')

	def _flickr_on_auth(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Flickr authentication failed')

		flkr_access = models.userinfo.FlickrAccessToken(
			username = user["access_token"]["username"],
			secret = user["access_token"]["secret"],
			fullname = user["access_token"]["fullname"],
			key = user["access_token"]["key"],
			user_nsid = user["access_token"]["user_nsid"]
		)

		flkr = models.userinfo.FlickrUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			flickr_access_token = flkr_access,
			flickr_stat = user["stat"],
			flickr_user_url = user["user"]["url"],
			flickr_nsid = user["user"]["nsid"]
		)

		user_obj = models.userinfo.User.objects(username=self.get_secure_cookie("username"))
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

		self.write( json.dumps( user ))
		self.finish()

		# self.render('test.html', user=user)


class KhanAcademyHandler(tornado.web.RequestHandler, mixins.KhanAcademyMixin):
	@tornado.web.asynchronous
	def get(self):
		oAuthToken = self.get_secure_cookie('khanacademy_oauth_token')
		oAuthSecret = self.get_secure_cookie('khanacademy_oauth_secret')

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

		self.khanacademy_authorize_redirect('http://localhost:8000/v1/khanacademy')  # Khan Academy requires a callback url

	def _khanacademy_on_auth(self, user):
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Khan Academy authentication failed')

		# self.write(json.dumps(user))
		# self.finish()

		ka_access = models.userinfo.KhanAcademyAccessToken(
			khanacademy_secret = user["access_token"]["secret"],
			khanacademy_key = user["access_token"]["key"],
		)

		ka = models.userinfo.KhanAcademyUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			khanacademy_has_notification = None,
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

		user_obj = models.userinfo.User.objects(username=self.get_secure_cookie("username"))
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


class OpenPathsHandler(BaseHandler):
	# @tornado.web.authenticated
	@tornado.web.asynchronous
	def get(self):
		# username = self.get_secure_cookie("username")
		username = "pdarche"
		user = models.userinfo.User.objects(username=username)[0]

		if user.openpaths_user_info == None:
			self.write("open paths not connected")
		else:
			self.write("user already connected")

		self.finish()

	def post(self):
		username = "pdarche"
		user = models.userinfo.User.objects(username=username)[0]
		access_key = self.get_argument("access_key")
		access_secret = self.get_argument("access_secret")
		# username = self.get_secure_cookie("username")

		op = models.userinfo.OpenPathsUserInfo(
			created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%m:%s"),
			op_access_key = access_key,
			op_access_secret = access_secret
		)

		user.openpaths_user_info = op

		if user.save():
			response = "saved"
			print "openpaths userinfo saved"
		else:
			print "openpaths userinfo not saved"
			response = "not saved"

		self.write(response)
		self.finish()


class WithingsHandler(tornado.web.RequestHandler, mixins.WithingsMixin): 
	@tornado.web.asynchronous
	def get(self):
		oAuthToken = self.get_secure_cookie('zeo_oauth_token')
		oAuthSecret = self.get_secure_cookie('zeo_oauth_secret')
		userID = self.get_secure_cookie('zeo_user_id')

		if self.get_argument('oauth_token', None):	
			self.get_authenticated_withings_user(self.async_callback(self._withings_on_auth))
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

		callback_uri = { "oauth_callback" : "http://localhost:8000/v1/withings" }
		self.authorize_withings_redirect(extra_params=callback_uri)

	def _withings_on_auth(self, user):		
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500, 'Withings authentication failed')

		self.write( json.dumps(user) )
		self.finish()
		# self.render('test.html', user=json.dumps(user))


####### REFACTOR.  THIS IS TERRIBLE
class FitbitImportHandler(BaseHandler, mixins.FitbitMixin):	
	# if user.ftbt_user_info != None:
	activities = []
	foods = []
	sleep = []
	body = []

	@tornado.web.authenticated
	@tornado.web.asynchronous
	def get(self):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/activities/steps/date/%s/today' % memberSince,
			access_token = accessToken,
			user_id = userID,
			callback = self.async_callback(self._on_steps)
		)
		return

	def _on_steps(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/activities/calories/date/%s/today' % memberSince,
			access_token = accessToken,
			user_id = userID,
			callback = self.async_callback(self._on_calories)
		)
		self.activities.append(data)

	def _on_calories(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/activities/distance/date/%s/today' % memberSince,
			access_token = accessToken,
			user_id = userID,
			callback = self.async_callback(self._on_distance)
		)
		self.activities.append(data)


	def _on_distance(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/activities/floors/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_floors)
		)
		self.activities.append(data)

	def _on_floors(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/activities/elevation/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_elevation)
		)
		self.activities.append(data)

	def _on_elevation(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/activities/minutesSedentary/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_mins_sedentary)
		)
		self.activities.append(data)

	def _on_mins_sedentary(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/activities/minutesLightlyActive/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_mins_lightly_active)
		)
		self.activities.append(data)

	def _on_mins_lightly_active(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/activities/minutesFairlyActive/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_mins_fairly_active)
		)
		self.activities.append(data)

	def _on_mins_fairly_active(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/activities/minutesVeryActive/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_mins_highly_active)
		)
		self.activities.append(data)

	def _on_mins_highly_active(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/sleep/startTime/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_sleep_start_time)
		)
		self.activities.append(data)

	# def _on_active_score(self, data):
	# 	accessToken = self.get_access_token()
	# 	memberSince = self.get_member_since()
	# 	userID = self.get_user_id()

	# 	self.fitbit_request('/user/-/activities/activityCalories/date/%s/today' % memberSince,
	# 		access_token =  accessToken,
	# 		user_id =		userID,
	# 		callback = 		self.async_callback(self._on_sleep_start_time)
	# 	)
	# 	self.activities.append(data)

	def _on_sleep_start_time(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/sleep/timeInBed/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_time_in_bed)
		)
		self.sleep.append(data)

	def _on_time_in_bed(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/sleep/minutesAsleep/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_minutes_asleep)
		)
		self.sleep.append(data)

	def _on_minutes_asleep(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/sleep/awakeningsCount/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_awakenings_count)
		)
		self.sleep.append(data)

	def _on_awakenings_count(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/sleep/minutesAwake/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_minutes_awake)
		)
		self.sleep.append(data)

	def _on_minutes_awake(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/sleep/minutesToFallAsleep/date/%s/today' % memberSince,
			access_token =  accessToken,
			user_id =		userID,
			callback = 		self.async_callback(self._on_minutes_to_fall_asleep)
		)
		self.sleep.append(data)

	def _on_minutes_to_fall_asleep(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/sleep/minutesAfterWakeup/date/%s/today' % memberSince,
			access_token = accessToken,
			user_id = userID,
			callback = self.async_callback(self._on_minutes_after_wakeup)
		)
		self.sleep.append(data)

	def _on_minutes_after_wakeup(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/sleep/efficiency/date/%s/today' % memberSince,
			access_token = accessToken,
			user_id = userID,
			callback = self.async_callback(self._on_efficiency)
		)
		self.sleep.append(data)

	def _on_efficiency(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/body/weight/date/%s/today' % memberSince,
			access_token = accessToken,
			user_id = userID,
			callback = self.async_callback(self._on_weight)
		)
		self.sleep.append(data)

	def _on_weight(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/body/bmi/date/%s/today' % memberSince,
			access_token = accessToken,
			user_id = userID,
			callback = self.async_callback(self._on_bmi)
		)
		self.body.append(data)

	def _on_bmi(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/body/fat/date/%s/today' % memberSince,
			access_token = accessToken,
			user_id = userID,
			callback = self.async_callback(self._on_fat)
		)
		self.body.append(data)

	def _on_fat(self, data):
		accessToken = self.get_access_token()
		memberSince = self.get_member_since()
		userID = self.get_user_id()

		self.fitbit_request('/user/-/body/fat/date/%s/today' % memberSince,
			access_token = accessToken,
			user_id = userID,
			callback = self.async_callback(self._on_imported)
		)
		self.body.append(data)

	def _on_imported(self, data):

		print " activities stuff thing"
		print self.activities[1]

		self.body.append(data)

		dates = self.activities[0]["activities-steps"]
		steps = self.activities[0]["activities-steps"]
		calories = self.activities[1]["activities-calories"]
		distance = self.activities[2]["activities-distance"]
		floors = self.activities[3]["activities-floors"]
		elevation = self.activities[4]["activities-elevation"]
		mins_sedentary = self.activities[5]["activities-minutesSedentary"]
		mins_light = self.activities[6]["activities-minutesLightlyActive"]
		mins_fair = self.activities[7]["activities-minutesFairlyActive"]
		mins_very = self.activities[8]["activities-minutesVeryActive"]

		zipped_activities = zip(
			dates, steps, calories, distance, floors,
			elevation, mins_sedentary, mins_light,
			mins_fair, mins_very
		)

		for day in zipped_activities:
			activity_record = models.fitbit.FitbitPhysicalActivity(
				phro_created_at = int(time.time()),
				username = self.get_secure_cookie("username"),
				created_at = day[0]["dateTime"],
				ftbt_steps = int(day[1]["value"]),
				ftbt_distance = float(day[3]["value"]),
				ftbt_calories_out = int(day[2]["value"]),
				ftbt_activity_calories = None,
				ftbt_floors = int(day[4]["value"]),
				ftbt_elevation = float(day[5]["value"]),
				ftbt_mins_sedentary = int(day[6]["value"]),
				ftbt_mins_lightly_active = int(day[7]["value"]),
				ftbt_mins_fairly_active = int(day[8]["value"]),
				ftbt_mins_very_active = int(day[9]["value"]),
				ftbt_active_score = None,
				ftbt_activities = None
			)

			if activity_record.save():
				print "saved activity record"
			else:
				print "didn't save activities"


		created_at = self.sleep[0]["sleep-startTime"]
		start_time = self.sleep[0]["sleep-startTime"]
		time_in_bed = self.sleep[1]["sleep-timeInBed"]
		minutes_asleep = self.sleep[2]["sleep-minutesAsleep"]
		awakenings_count = self.sleep[3]["sleep-awakeningsCount"]
		minutes_awake = self.sleep[4]["sleep-minutesAwake"]
		minutes_to_fall_asleep = self.sleep[5]["sleep-minutesToFallAsleep"]
		minutes_after_wakeup = self.sleep[6]["sleep-minutesAfterWakeup"]
		efficiency = self.sleep[7]["sleep-efficiency"]

		zipped_sleep = zip(
			created_at, start_time, time_in_bed, 
			minutes_asleep, awakenings_count, minutes_awake,
			minutes_to_fall_asleep, minutes_after_wakeup,
			efficiency
		)

		for sleep_day in zipped_sleep:
			sleep_record = models.fitbit.FitbitSleep(
				phro_created_at = int(time.time()),
				username = self.get_secure_cookie("username"),
				created_at = sleep_day[0]["dateTime"],
				ftbt_start_time = sleep_day[1]["value"],
				ftbt_time_in_bed = sleep_day[2]["value"],
				ftbt_minutes_asleep = int(sleep_day[3]["value"]),
				ftbt_awakenings_count = int(sleep_day[4]["value"]),
				ftbt_minutes_awake = int(sleep_day[5]["value"]),
				ftbt_minutes_to_fall_asleep = int(sleep_day[6]["value"]),
				ftbt_minutes_after_wakeup = int(sleep_day[7]["value"]),
				ftbt_efficiency = int(sleep_day[8]["value"])
			)

			if sleep_record.save():
				print "saved sleep record"
			else:
				print "didn't save sleep record"


		created_at = self.body[0]["body-weight"]
		weight = self.body[0]["body-weight"]
		bmi = self.body[1]["body-bmi"]
		fat = self.body[2]["body-fat"]

		zipped_body = zip(
			created_at, weight,
			bmi, fat 
		)

		for body_day in zipped_body:
			body_record = models.fitbit.FitbitBodyData(
				phro_created_at = int(time.time()),
				username = self.get_secure_cookie("username"),
				created_at = body_day[0]["dateTime"],
				ftbt_weight =  float(body_day[1]["value"]),
				ftbt_bmi = float(body_day[2]["value"]),
				ftbt_fat = float(body_day[3]["value"])
			)

			if body_record.save():
				print "saved body record"
			else:
				print "didn't save body record"			

		self.write( "success" )
		self.finish()

	def get_access_token(self):
		curr_user = models.userinfo.User.objects(username=self.get_secure_cookie("username"))[0]

		if hasattr(curr_user["ftbt_user_info"], "ftbt_access_token"):
			oAuthToken = curr_user["ftbt_user_info"]["ftbt_access_token"]["key"]
			oAuthSecret = curr_user["ftbt_user_info"]["ftbt_access_token"]["secret"]
			userID = curr_user["ftbt_user_info"]["ftbt_access_token"]["encoded_user_id"]			

			accessToken = {
				'key': 		oAuthToken,
				'secret':	oAuthSecret
			}

			return accessToken

		else:
			self.redirect('/fitbit')

	def get_member_since(self):
		curr_user = models.userinfo.User.objects(username=self.get_secure_cookie("username"))[0]
		return curr_user["ftbt_user_info"]["ftbt_member_since"]

	def get_user_id(self):
		curr_user = models.userinfo.User.objects(username=self.get_secure_cookie("username"))[0]
		return curr_user["ftbt_user_info"]["ftbt_access_token"]["encoded_user_id"]


class FoursquareImportHandler(BaseHandler, mixins.FoursquareMixin):
	@tornado.web.authenticated
	@tornado.web.asynchronous
	def get(self):
		user_info = self.get_fs_user_info()
		user_id = user_info["user_id"]
		access_token = user_info["access_token"]


		#NOTE : THIS IS SO FUCKING JANKY.  THIS NEEDS TO BE DONE WITH TORNADO.GEN 
		self.foursquare_request(
		    path="/users/self/checkins",
		    args= { "limit" : 250 },
		    callback=self.async_callback(self._on_imported),
		    access_token=access_token
		)

		self.foursquare_request(
		    path="/users/self/checkins",
		    args= { "offset" : 250, "limit" : 250 },
		    callback=self.async_callback(self._on_imported),
		    access_token=access_token
		)

		self.foursquare_request(
		    path="/users/self/checkins",
		    args= { "offset" : 500, "limit" : 250 },
		    callback=self.async_callback(self._on_imported),
		    access_token=access_token
		)

		self.foursquare_request(
		    path="/users/self/checkins",
		    args= { "offset" : 750, "limit" : 250 },
		    callback=self.async_callback(self._on_last_imported),
		    access_token=access_token
		)
		
		# response = yield tornado.gen.Task(
		# 	self.foursquare_request,
		#     path="/users/self/checkins",
		#     args= { "limit" : 250 },
		#     access_token=access_token
		# )

		# response = { "derp" : "derp" }
		
	def _on_test(self, checkins):
		self.write(json.dumps(checkins))
		self.finish()

	def _on_imported(self, checkins):
		user_info = self.get_fs_user_info()
		user_id = user_info["user_id"]
		
		checkins = checkins["response"]["checkins"]["items"]

		for index, checkin in enumerate(checkins):

			if "stats" in checkin["venue"].keys():
				print "has venue stats"	
				venue_stats =models.foursquare.VenueStats(
					checkins_count = checkin["venue"]["stats"]["checkinsCount"] if "checkinsCount" in checkin["venue"]["stats"].keys() else None,
					users_count = checkin["venue"]["stats"]["usersCount"] if "userCount" in checkin["venue"]["stats"].keys() else None,
					tips_count = checkin["venue"]["stats"]["tipsCount"] if "tipsCount" in checkin["venue"]["stats"].keys() else None
				)

			else:
				venue_stats = None

			if "beenHere" in checkin.keys():
				print "has venue been here"
				been_here = models.foursquare.VenueBeenHere(
					count = checkin["beenHere"]["count"] if "count" in checkin["beenHere"].keys() else None,
					marked = checkin["beenHere"]["marked"] if "marked" in checkin["beenHere"].keys() else None
				)

			else:
				been_here = None
			
			if "likes" in checkin["venue"].keys():	
				print "has venue likes"
				likes = models.foursquare.VenueLikes(
					type = checkin["venue"]["type"] if "type" in checkin["venue"].keys() else None,
					count = checkin["venue"]["count"] if "count" in checkin["venue"].keys() else None,
					summry = checkin["venue"]["summary"] if "summary" in checkin["venue"].keys() else None
				)

			else:
				likes = None

			if "contact" in checkin["venue"].keys():
				print "has venue contact"	
				contact  = models.foursquare.VenueContact(
					phone = checkin["venue"]["contact"]["phone"] if "phone" in checkin["venue"]["contact"].keys() else None,
					formatted_phone = checkin["venue"]["contact"]["formattedPhone"] if "formattedPhone" in checkin["venue"]["contact"].keys() else None,
					twitter = checkin["venue"]["contact"]["twitter"] if "twitter" in checkin["venue"]["contact"].keys() else None,
					facebook = checkin["venue"]["contact"]["facebook"] if "facebook" in checkin["venue"]["contact"].keys()
					 else None
				)

			else :
				contact = None

			if "menu" in checkin["venue"].keys():
				print "has venue menu"
				venue_menu = models.foursquare.VenueMenu(
					url = checkin["venue"]["menu"]["url"] if "url" in checkin["venue"]["menu"].keys() else None,
					mobileUrl = checkin["venue"]["menu"]["mobileUrl"] if "url" in checkin["venue"]["menu"].keys() else None,
					type = checkin["venue"]["menu"]["mobileUrl"] if "type" in checkin["venue"]["menu"].keys() else None
				)

			else:
				venue_menu = None

			if "location" in checkin["venue"].keys():
				print "has venue location"
				location = models.foursquare.VenueLocation(
					address = checkin["venue"]["location"]["address"] if "address" in checkin["venue"]["location"].keys() else None,
					cross_street = checkin["venue"]["location"]["crossStreet"] if "crossStreet" in checkin["venue"]["location"].keys() else None,
					lat = checkin["venue"]["location"]["lat"] if "lat" in checkin["venue"]["location"].keys() else None,
					lng = checkin["venue"]["location"]["lng"] if "lng" in checkin["venue"]["location"].keys() else None,
					postal_code = checkin["venue"]["location"]["postalCode"] if "postalCode" in checkin["venue"]["location"].keys() else None,
					city = checkin["venue"]["location"]["city"] if "city" in checkin["venue"]["location"].keys() else None,
					state = checkin["venue"]["location"]["state"] if "state" in checkin["venue"]["location"].keys() else None,
					country = checkin["venue"]["location"]["country"] if "country" in checkin["venue"]["location"].keys() else None,
					cc = checkin["venue"]["location"]["cc"] if "cc" in checkin["venue"]["location"].keys() else None
				)
			
			else:
				location = None

			if "venue" in checkin.keys():
				print "has venue"
				venue = models.foursquare.Venue(
					venue_id = checkin["venue"]["id"] if "venueId" in checkin["venue"].keys() else None,
					name = checkin["venue"]["name"] if "name" in checkin["venue"].keys() else None,
					contact = contact,
					location = location,
					cannonical_url = checkin["venue"]["cannonicalUrl"] if "cannonicalUrl" in checkin["venue"].keys() else None,
					categories = None, #LIST FIELD!!
					verified = checkin["venue"]["verified"] if "verified" in checkin["venue"].keys() else None,
					stats = venue_stats,
					url = checkin["venue"]["url"] if "url" in checkin["venue"].keys() else None,
					likes = likes,
					like = checkin["venue"]["like"] if "like" in checkin["venue"].keys() else None,				
					menu = venue_menu,
				)

			else:
				print "doesn't have venue"
				venue = None

			checkIn = models.foursquare.CheckIn(				
				id = objectid.ObjectId(),
				phro_created_at = int(time.time()),
				username = self.get_secure_cookie("username"),
				record_created_at = checkin["createdAt"],
				fs_id = checkin["id"],
				fs_created_at = checkin["createdAt"],
				fs_type = checkin["type"],
				fs_timezone_offset = checkin["timeZoneOffset"],
				fs_timezone = checkin["timeZone"],
				fs_venue = venue,
				fs_like = checkin["like"],
				fs_likes = None
			)

			if checkIn.save():
				print "checkin saved"
			else:
				print "checkin didn't save"


	def _on_last_imported(self, checkins):
		user_info = self.get_fs_user_info()
		user_id = user_info["user_id"]
		
		checkins = checkins["response"]["checkins"]["items"]

		for index, checkin in enumerate(checkins):

			if "stats" in checkin["venue"].keys():
				print "has venue stats"	
				venue_stats =models.foursquare.VenueStats(
					checkins_count = checkin["venue"]["stats"]["checkinsCount"] if "checkinsCount" in checkin["venue"]["stats"].keys() else None,
					users_count = checkin["venue"]["stats"]["usersCount"] if "userCount" in checkin["venue"]["stats"].keys() else None,
					tips_count = checkin["venue"]["stats"]["tipsCount"] if "tipsCount" in checkin["venue"]["stats"].keys() else None
				)

			else:
				venue_stats = None

			if "beenHere" in checkin.keys():
				print "has venue been here"
				been_here = models.foursquare.VenueBeenHere(
					count = checkin["beenHere"]["count"] if "count" in checkin["beenHere"].keys() else None,
					marked = checkin["beenHere"]["marked"] if "marked" in checkin["beenHere"].keys() else None
				)

			else:
				been_here = None
			
			if "likes" in checkin["venue"].keys():	
				print "has venue likes"
				likes = models.foursquare.VenueLikes(
					type = checkin["venue"]["type"] if "type" in checkin["venue"].keys() else None,
					count = checkin["venue"]["count"] if "count" in checkin["venue"].keys() else None,
					summry = checkin["venue"]["summary"] if "summary" in checkin["venue"].keys() else None
				)

			else:
				likes = None

			if "contact" in checkin["venue"].keys():
				print "has venue contact"	
				contact  = models.foursquare.VenueContact(
					phone = checkin["venue"]["contact"]["phone"] if "phone" in checkin["venue"]["contact"].keys() else None,
					formatted_phone = checkin["venue"]["contact"]["formattedPhone"] if "formattedPhone" in checkin["venue"]["contact"].keys() else None,
					twitter = checkin["venue"]["contact"]["twitter"] if "twitter" in checkin["venue"]["contact"].keys() else None,
					facebook = checkin["venue"]["contact"]["facebook"] if "facebook" in checkin["venue"]["contact"].keys()
					 else None
				)

			else :
				contact = None

			if "menu" in checkin["venue"].keys():
				print "has venue menu"
				venue_menu = models.foursquare.VenueMenu(
					url = checkin["venue"]["menu"]["url"] if "url" in checkin["venue"]["menu"].keys() else None,
					mobileUrl = checkin["venue"]["menu"]["mobileUrl"] if "url" in checkin["venue"]["menu"].keys() else None,
					type = checkin["venue"]["menu"]["mobileUrl"] if "type" in checkin["venue"]["menu"].keys() else None
				)

			else:
				venue_menu = None

			if "location" in checkin["venue"].keys():
				print "has venue location"
				location = models.foursquare.VenueLocation(
					address = checkin["venue"]["location"]["address"] if "address" in checkin["venue"]["location"].keys() else None,
					cross_street = checkin["venue"]["location"]["crossStreet"] if "crossStreet" in checkin["venue"]["location"].keys() else None,
					lat = checkin["venue"]["location"]["lat"] if "lat" in checkin["venue"]["location"].keys() else None,
					lng = checkin["venue"]["location"]["lng"] if "lng" in checkin["venue"]["location"].keys() else None,
					postal_code = checkin["venue"]["location"]["postalCode"] if "postalCode" in checkin["venue"]["location"].keys() else None,
					city = checkin["venue"]["location"]["city"] if "city" in checkin["venue"]["location"].keys() else None,
					state = checkin["venue"]["location"]["state"] if "state" in checkin["venue"]["location"].keys() else None,
					country = checkin["venue"]["location"]["country"] if "country" in checkin["venue"]["location"].keys() else None,
					cc = checkin["venue"]["location"]["cc"] if "cc" in checkin["venue"]["location"].keys() else None
				)
			
			else:
				location = None

			if "venue" in checkin.keys():
				print "has venue"
				venue = models.foursquare.Venue(
					venue_id = checkin["venue"]["id"] if "venueId" in checkin["venue"].keys() else None,
					name = checkin["venue"]["name"] if "name" in checkin["venue"].keys() else None,
					contact = contact,
					location = location,
					cannonical_url = checkin["venue"]["cannonicalUrl"] if "cannonicalUrl" in checkin["venue"].keys() else None,
					categories = None, #LIST FIELD!!
					verified = checkin["venue"]["verified"] if "verified" in checkin["venue"].keys() else None,
					stats = venue_stats,
					url = checkin["venue"]["url"] if "url" in checkin["venue"].keys() else None,
					likes = likes,
					like = checkin["venue"]["like"] if "like" in checkin["venue"].keys() else None,				
					menu = venue_menu,
				)

			else:
				print "doesn't have venue"
				venue = None

			checkIn = models.foursquare.CheckIn(				
				id = objectid.ObjectId(),
				phro_created_at = int(time.time()),
				username = self.get_secure_cookie("username"),
				record_created_at = checkin["createdAt"],
				fs_id = checkin["id"],
				fs_created_at = checkin["createdAt"],
				fs_type = checkin["type"],
				fs_timezone_offset = checkin["timeZoneOffset"],
				fs_timezone = checkin["timeZone"],
				fs_venue = venue,
				fs_like = checkin["like"],
				fs_likes = None
			)

			if checkIn.save():
				print "checkin saved"
			else:
				print "checkin didn't save"

		self.write("success")
		self.finish()

	# def _on_test(self, checkins):
	# 	self.write( checkins )
	# 	self.finish()


	def get_fs_user_info(self):
		curr_user = models.userinfo.User.objects(username=self.get_secure_cookie("username"))[0]

		if hasattr(curr_user["foursquare_user_info"], "foursquare_access_token"):
			access_token = curr_user["foursquare_user_info"]["foursquare_access_token"]
			user_id = curr_user["foursquare_user_info"]["foursquare_id"]

			user_info = { "access_token" : access_token, "user_id" : user_id }

			return user_info

		else:
			self.redirect('/v1/foursquare')



class OpenPathsImportHandler(BaseHandler):
	@tornado.web.authenticated
	@tornado.web.asynchronous
	def get(self):
		username = self.get_secure_cookie("username")
		user = models.userinfo.User.objects(username=username)[0]

		ACCESS = user["openpaths_user_info"]["op_access_key"]
		SECRET = user["openpaths_user_info"]["op_access_secret"]
		URL = "https://openpaths.cc/api/1" 

		def build_auth_header(url, method):
		    params = {                                            
		        'oauth_version': "1.0",
		        'oauth_nonce': oauth2.generate_nonce(),
		        'oauth_timestamp': int(time.time()),
		    }
		    consumer = oauth2.Consumer(key=ACCESS, secret=SECRET)
		    params['oauth_consumer_key'] = consumer.key 
		    request = oauth2.Request(method=method, url=url, parameters=params)    
		    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
		    request.sign_request(signature_method, consumer, None)
		    return request.to_header()

		# GET data (last 24 hours)
		now = time.time()
		params = { 'num_points' : 2000 }    # get the last 2000 points
		query = "%s?%s" % (URL, urllib.urlencode(params))
		print(query)
		try:
		    request = urllib2.Request(query)
		    request.headers = build_auth_header(URL, 'GET')
		    connection = urllib2.urlopen(request)
		    data = json.loads(''.join(connection.readlines()))
		    
		    for record in data:
		    	location = models.openpaths.OpenPathsLocation(
		    		phro_created_at = int(time.time()),
		    		username = username,
		    		device = record["device"],
		    		os = record["os"],
		    		t = record["t"],
		    		lat = record["lat"],
		    		lon = record["lon"],
		    		alt = record["alt"]
		    	)

		    	if location.save():
		    		print "op location saved"
		    	else:
		    		print "op location not saved"

		    self.write("success")
		    self.finish()

		except urllib2.HTTPError as e:
		    print(e.read())
		    self.write("error")
		    self.finish()

class FlickrImportHandler(BaseHandler, mixins.FlickrMixin):
	geo = None
	photos = []
	@tornado.web.authenticated
	@tornado.web.asynchronous
	def get(self):
		username = self.get_secure_cookie("username")
		user = models.userinfo.User.objects(username=username)[0]
		access_token = user["flickr_user_info"]["flickr_access_token"]

		self.flickr_request(
			format="json",
			api_key=self.settings["flickr_consumer_key"],
			nojsoncallback="1", 
			method="flickr.photos.getWithGeoData",
			per_page = 500,
			access_token=access_token,
			callback=self.async_callback(self._on_geo_one)
		)

	
	def _on_geo_one(self, data):
		username = self.get_secure_cookie("username")
		user = models.userinfo.User.objects(username=username)[0]
		access_token = user["flickr_user_info"]["flickr_access_token"]
		
		print "pages are %r" % data
		self.geo = data

		for photo in self.geo["photos"]["photo"]:
			pic = models.flickr.FlickrPhoto(
				phro_created_at = int(time.time()),
				username = self.get_secure_cookie("username"),
				photo_id = photo["id"],
				owner = photo["owner"],
				secret = photo["secret"],
				server = photo["server"],
				farm = photo["farm"],
				title = photo["title"],
				is_public = photo["ispublic"],
				is_friend = photo["isfriend"],
				is_family = photo["isfamily"],
				has_geo = True
			)

			if pic.save():
				print "geo saved"
			else:
				print "geo not saved"

		self.flickr_request(
			format="json",
			api_key=self.settings["flickr_consumer_key"],
			nojsoncallback="1", 
			method="flickr.photos.getWithoutGeoData",
			access_token=access_token,
			callback=self.async_callback(self._on_geo_two)
		)

	def _on_geo_two(self, data):
		username = self.get_secure_cookie("username")
		user = models.userinfo.User.objects(username=username)[0]
		access_token = user["flickr_user_info"]["flickr_access_token"]
		
		print "pages are %r" % data
		self.geo = data

		for photo in self.geo["photos"]["photo"]:
			pic = models.flickr.FlickrPhoto(
				phro_created_at = int(time.time()),
				username = self.get_secure_cookie("username"),
				photo_id = photo["id"],
				owner = photo["owner"],
				secret = photo["secret"],
				server = photo["server"],
				farm = photo["farm"],
				title = photo["title"],
				is_public = photo["ispublic"],
				is_friend = photo["isfriend"],
				is_family = photo["isfamily"],
				has_geo = True
			)

			if pic.save():
				print "geo saved"
			else:
				print "geo not saved"

		self.flickr_request(
			format="json",
			api_key=self.settings["flickr_consumer_key"],
			nojsoncallback="1", 
			method="flickr.photos.getWithoutGeoData",
			access_token=access_token,
			callback=self.async_callback(self._on_non_geo)
		)

	def _on_non_geo(self, data):
		username = self.get_secure_cookie("username")
		user = models.userinfo.User.objects(username=username)[0]
		access_token = user["flickr_user_info"]["flickr_access_token"]

		for photo in data["photos"]["photo"]:
			pic = models.flickr.FlickrPhoto(
				phro_created_at = int(time.time()),
				username = self.get_secure_cookie("username"),
				photo_id = photo["id"],
				owner = photo["owner"],
				secret = photo["secret"],
				server = photo["server"],
				farm = photo["farm"],
				title = photo["title"],
				is_public = photo["ispublic"],
				is_friend = photo["isfriend"],
				is_family = photo["isfamily"],
				has_geo = False
			)

			if pic.save():
				print "non-geo saved"
			else:
				print "non-geo not saved"

		self.write("success")
		self.finish()

	def push_to_ar(self, photo):
		self.photos.append(photo)


class RemoveUserHandler(tornado.web.RequestHandler):
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		
		user = models.userinfo.User.objects(username=username, password=password)

		user[0].delete(safe=True)
		self.write("user deleted\n")

		#add functionality for deleting all records


class DocumentationHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("docs.html")


class PrintAppSettings(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		key = models.models.AppSettings.objects[0],
		for k in key[0]:
			print "%s, %s" % (k, key[0][k])
		# secret = models.models.AppSettings.objects[0]

		# data = { "key" : key, "secret" : secret }

		# self.write(json.dumps(data))
		# self.finish()


class PresentationHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render("presentation.html")


class DataHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, input):
		input = input.split('/',1)
		path = input[1].encode('utf-8')
		username = input[0].encode('utf-8')
		params = self.request.arguments
		params["username"] = [username]

		order_by = self.order(params)
		limit = self.limit(params)
		kw = keyword_args(params)

		paths = { 
			"body/physicalActivity" : physact.PhysicalActivity,
			"body/sleep" : models.sleep.SleepRecord,
			"body/nutrition" : nutrition.NutritionRecord,
			"body/location" : loc.Location,
			"traits/healthy" : None,
			"traits/sustainable" : None,
			"traits/educated" : None, 
			"traitSpecific/cardiovascular" : None,
			"traitSpecific/musculoskelatal" : None, 
			"traitSpecific/respirator" : None,
			"traitSpecific/mental" : None
		}

		if order_by != None:
			print "orderby is %s" % order_by
			objs = paths[path].objects(**kw).order_by(order_by)
		else:
			objs = paths[path].objects(**kw)

		if limit != None:
			objs = objs[:limit]

		data = json.dumps(objs, default=encode_model)
		self.write( data )

	def order(self, params):
		order_by = None		
		if "order_by" in params.keys():
			split = params["order_by"][0].split('__')
			if split[1] == "desc":
				order_by = "-%s" % split[0]
			else:
				order_by = "+%s" % split[0]

			del params["order_by"]

		return order_by
			
	def limit(self, params):
		limit = None
		if "limit" in params.keys():
			limit = int(params["limit"][0])
			del params["limit"]

		return limit

	def post(self, input):
		path = input.encode('utf-8')

		paths = { 
			"body/physicalActivity" : physact.PhysicalActivity,
			"body/sleep" : models.sleep.SleepRecord,
			"body/nutrition" : nutrition.NutritionRecord,
			"body/location" : loc.Location
		}

		objDict = json.loads(self.request.body)
		id_str = objDict["null"]
		doc = nutrition.NutritionRecord.objects( #GENERALIZE
					id=objectid.ObjectId(id_str))[0]

		# this is a hack
		docDict = json.loads(json.dumps(doc, default=encode_model))

		diff = DictDiffer(objDict, docDict)
		changedKeys = list(diff.changed())

		for change in changedKeys:
			if change != 'ingredients':
				updateString = 'set__%s' % change
				kw = { updateString : objDict[change] }
				doc.update(**kw)
			else:
				a = [ json.loads(json.dumps(x, default=encode_model)) 
							for x in doc.ingredients ]
				b = objDict["ingredients"]
				
				objNames = [ ( i, objDict["name"] ) for i, objDict in enumerate(a) ]
				docNames = [ ( i, docDict["name"] ) for i, docDict in enumerate(b) ]
				
				s = set(objNames)
				new_ingredients = [x for x in docNames if x not in s]

				for new_ingredient in new_ingredients:					
					ingredient = b[new_ingredient[0]]

					mealIngredient = nutrition.MealIngredient(
							name = ingredient['name'],
							brand = ingredient['brand'],
							item_description = ingredient['item_description'],
							ingredient_statement = ingredient['ingredient_statement'],
							calories = ingredient['calories'],
							calories_from_fat = ingredient['calories_from_fat'],
							total_fat = ingredient['total_fat'],
							monounsaturated_fat = ingredient['monounsaturated_fat'],
							polyunsaturated_fat = ingredient['polyunsaturated_fat'],
							saturated_fat = ingredient['saturated_fat'],
							trans_fat = ingredient['trans_fat'],
							cholesterol = ingredient['cholesterol'],
							sodium = ingredient['sodium'],
							total_carbs = ingredient['total_carbs'],
							dietary_fiber = ingredient['dietary_fiber'],
							sugar = ingredient['sugar'],
							protein = ingredient['protein'],
							vit_a_dv = ingredient['vit_a_dv'],
							vit_c_dv = ingredient['vit_c_dv'],
							calcium_dv = ingredient['calcium_dv'],
							iron_dv = ingredient['iron_dv'],
							source = ingredient['source'],
							refuse_pct = ingredient['refuse_pct'],
							serving_size_qty = ingredient['serving_size_qty'],
							serving_size_unit = ingredient['serving_size_unit'],
							serving_weight_grams = ingredient['serving_weight_grams'],
							servings_per_container = ingredient['servings_per_container'],
							water_grams = ingredient['water_grams'],
							upc = ingredient['upc'],
							updated_at = ingredient['updated_at']
						)

					updateString = 'push__%s' % change
					kw = { updateString : mealIngredient}
					updated = doc.update(**kw)

					print "updated ingredient"


class RefHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, input):
		path = input
		params = self.request.arguments

		order_by = self.order(params)
		limit = self.limit(params)
		kw = keyword_args(params)

		paths = { 
			# "nutrition/des" : nutrition.SR25FoodDescription,
			# "nutrition/sr25" : nutrition.SR25Abbrev,
			# "nutrition/mypyramid" : pyramid.MyPyramidReferenceInfo,
			# "nutrition/standard_label" : nutrition.StandardNutritionLabelMealItem,			
			"traits" : healthy.Trait,
			"traits/traitSpecifics" : healthy.TraitSpecific,
			"traits/traitSpecifics/recommendedHabit" : healthy.RecommendedHabit,
			"traits/traitSpecifics/recommendedHabit/currentStatus" : healthy.CurrentStatus,
			"traits/traitSpecifics/recommendedHabit/actionsToTake" : healthy.ActionToTake,
			"traits/traitSpecifics/recommendedHabit/triggers" : healthy.Trigger,
			"traits/traitSpecifics/studies" : healthy.Study
		}

		if order_by != None:
			objs = paths[path].objects(**kw).order_by(order_by)
		else:
			objs = paths[path].objects(**kw)

		if limit != None:
			objs = objs[:limit]

		print "there are %s objects" % len(objs)

		data = json.dumps(objs, default=encode_model)
		self.write(data)


	def order(self, params):
		order_by = None		
		if "order_by" in params.keys():
			split = params["order_by"][0]
			if split == "desc":
				print "descending"
				order_by = "-%s" % split[0]
			else:
				print "acending"
				order_by = "+%s" % split[0]

			del params["order_by"]

		return order_by
			
	def limit(self, params):
		limit = None
		if "limit" in params.keys():
			limit = int(params["limit"][0])
			del params["limit"]

		return limit

	def post(self, input):
		print input
		print self.request.arguments
		params = self.request.arguments 

		paths = {
			"traits/traitSpecifics/recommendedHabit/triggers" : healthy.Trigger
		}

		trigger = healthy.Trigger(
			username = "pdarche",
			triggerd_distance = float(params["trigger_distance"][0]),
			trigger_location = params["trigger_location"][0],
			trigger_text = params["trigger_text"][0],
			for_rec_habit_key = params["for_rec_habit_key"][0]
		)

		if trigger.save():
			print "saved"
		else:
			print "didn't save"

class DumpHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, input):
		username = self.get_secure_cookie('username')
		paths = {
			"physicalActivity" : physact.PhysicalActivity,
			"sleep" : models.sleep.SleepRecord,
			"location" : loc.Location,
			"nutrition" : nutrition.NutritionRecord,
			"zeo" : models.zeo.ZeoSleepRecord,
			"flickr" : models.flickr.FlickrPhoto,
			"fitbit_activity" : models.fitbit.FitbitPhysicalActivity,
			"fitbit_sleep" : models.fitbit.FitbitSleep,
			"foursquare" : models.foursquare.CheckIn,
			"openpaths" : models.openpaths.OpenPathsLocation
		}

		objs = paths[input].objects()
		print len(objs)
		objs = json.dumps(objs, default=encode_model)
		self.write( objs )



class RemoveHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, input):
		username = self.get_secure_cookie('username')
		paths = {
			"physicalActivity" : physact.PhysicalActivity,
			"sleep" : models.sleep.SleepRecord,
			"location" : loc.Location,
			"nutrition" : nutrition.NutritionRecord,
			"zeo" : models.zeo.ZeoSleepRecord,
			"flickr" : models.flickr.FlickrPhoto,
			"fitbit_activity" : models.fitbit.FitbitPhysicalActivity,
			"fitbit_sleep" : models.fitbit.FitbitSleep,
			"foursquare" : models.foursquare.CheckIn,
			"openpaths" : models.openpaths.OpenPathsLocation,
			"traits" : healthy.Trait,
			"traitSpecifics" : healthy.TraitSpecific,
			"recommendedHabits" : healthy.RecommendedHabit,
			"currentStatuses" : healthy.CurrentStatus,
			"actionsToTake" : healthy.ActionToTake,
			"triggers" : healthy.Trigger
		}

		objs = paths[input].objects() #username=username
		objs.delete()
		self.write(str(len(objs)) + " records")

def keyword_args(kwargs):
	# kwargs is a dict of the keyword args passed to the function
	new_dict = dict()
	for key, value in kwargs.iteritems():
		new_dict[key] = value[0]
	return new_dict 

def walk(self, d, args):
	for arg in args:			
		if arg in d:
			if type(d[arg]) != type({}):
				self.callval = d[arg]						
			else:
				newd = d[arg]
				newargs = args[1:]
				self.walk(newd, newargs)
		else:
			break


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
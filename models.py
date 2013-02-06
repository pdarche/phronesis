#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

import logging

class AppSettings(Document):
	fitbit_consumer_key = StringField()
	fitbit_consumer_secret = StringField()
	twitter_consumer_key = StringField()
	twitter_consumer_secret = StringField()
	facebook_api_key = StringField()
	facebook_secret = StringField()
	zeo_consumer_key = StringField()
	zeo_consumer_secret = StringField()
	foursquare_api_key = StringField()
	foursquare_client_id = StringField()
	foursquare_client_secret = StringField()
	google_consumer_key = StringField()
	google_consumer_secret = StringField()
	flickr_consumer_key = StringField()
	flickr_consumer_secret = StringField()
	khanacademy_consumer_key = StringField()
	khanacademy_consumer_secret = StringField()
	cookie_secret = StringField()


################ SERVICE USER INFO ################
class FitbitAccessToken(EmbeddedDocument):
	key = StringField()
	encoded_user_id = StringField()
	secret = StringField()

class FitbitUserInfo(EmbeddedDocument):
	created_at = StringField()
	ftbt_user_name = StringField()
	ftbt_access_token = EmbeddedDocumentField(FitbitAccessToken)
	ftbt_weight_unit = StringField()
	ftbt_stride_length_walking = FloatField()
	ftbt_display_name = StringField()
	ftbt_foods_locale = StringField()
	ftbt_height_unit = StringField()
	ftbt_locale = StringField()
	ftbt_gender = StringField()
	ftbt_member_since = StringField()
	ftbt_offset_from_utc_millis = IntField()
	ftbt_encoded_id = StringField()
	ftbt_avatar = StringField()
	ftbt_water_unit = StringField()
	ftbt_distance_unit = StringField()
	ftbt_glucose_unit = StringField()
	ftbt_full_name = StringField()
	ftbt_nickname = StringField()
	ftbt_stride_length_running = FloatField()


class FoursquareUserInfo(EmbeddedDocument):
	created_at = StringField()
	foursquare_last_name = StringField()
	foursquare_first_name = StringField()
	foursquare_access_token = StringField()
	foursquare_user_photo = StringField()
	foursquare_pings = BooleanField()
	foursquare_home_city = StringField()
	foursquare_id = StringField()
	foursquare_bio = StringField()
	foursquare_relationship = StringField()
	foursquare_checkin_pings = StringField()


class FlickrAccessToken(EmbeddedDocument):
	flickr_username = StringField()
	flickr_secret = StringField()
	flickr_full_name = StringField()
	flickr_key = StringField()
	flickr_nsid = StringField()

class FlickrUserInfo(EmbeddedDocument):
	created_at = StringField() 			#add updates?
	flickr_access_token = EmbeddedDocumentField(FlickrAccessToken)
	flickr_stat = StringField()
	flickr_user_url = StringField()
	flickr_nsid = StringField()


class FacebookUserInfo(EmbeddedDocument):
	created_at = StringField()
	facebook_picture = StringField()
	facebook_first_name = StringField()
	facebook_last_name = StringField()
	facebook_name = StringField()
	facebook_locale = StringField()
	facebook_access_token = StringField()
	facebook_link = StringField()
	facebook_id = StringField()


class KhanAcademyAccessToken(EmbeddedDocument):
	khanacademy_secret = StringField()
	khanacademy_key = StringField()

class KhanAcademyUserInfo(EmbeddedDocument):
	created_at = StringField()
	khanacademy_has_notification = BooleanField()
	khanacademy_can_record_tutorial = BooleanField()
	khanacademy_is_demo = BooleanField()
	khanacademy_key_email = StringField()
	khanacademy_is_pre_phantom = BooleanField()
	khanacademy_developer = BooleanField()
	kahnacademy_user_id = StringField()
	khanacademy_is_google_user = BooleanField()
	khanacademy_profile_root = StringField()
	khanacademy_has_email_subscription = BooleanField()
	khanacademy_discussion_banned = BooleanField()
	khanacademy_is_phantom = BooleanField()
	khanacademy_email = StringField()
	khanacademy_is_facebook_user = BooleanField()
	khanacademy_is_midsignup_phantom = BooleanField()
	# khanacademy_auth_emails = ListField(StringField)
	khanacademy_last_modified_as_mapreduce_epoch = IntField()
	khanacademy_uservideocss_version = IntField()
	khanacademy_nickname = StringField()
	# khanacademy_user_input_auth_emails = ListField(StringField)
	khanacademy_kind = StringField()
	khanacademy_is_moderator_or_developer = BooleanField()
	khanacademy_joined = StringField()
	khanacademy_userprogresscache_version = IntField()
	khanacademy_gae_bingo_identity = StringField()


class TwitterUserInfo(EmbeddedDocument):
	created_at = StringField()
	twitter_default_profile_image = BooleanField()
	twitter_id = IntField()
	twitter_verified = BooleanField()
	twitter_profile_image_url_https = StringField()
	twitter_id_str = StringField()
	twitter_utc_offset = IntField()
	twitter_location = StringField()
	twitter_profile_image_url = StringField()
	twitter_geo_enabled = BooleanField()
	twitter_name = StringField()
	twitter_lang = StringField()
	twitter_screen_name = StringField()
	twitter_url = StringField()
	twitter_contributors_enabled = BooleanField() #remove?
	twitter_time_zone = StringField()
	twitter_protected = BooleanField()
	twitter_default_profile = BooleanField()	#remove?
	twitter_is_translator = BooleanField()		#remove?


class GoogleUserInfo(EmbeddedDocument):
	created_at = StringField()
	google_first_name = StringField()
	google_claimed_id = StringField()
	google_name = StringField()
	google_locale = StringField()
	google_last_name = StringField()
	google_email = StringField()


class User(Document):
	user_since = StringField()
	username = StringField()
	password = StringField()
	offset_from_utc_millis = IntField()
	time_zone = StringField()
	date_of_birth = DateTimeField()
	ftbt_user_info = EmbeddedDocumentField(FitbitUserInfo)
	foursquare_user_info = EmbeddedDocumentField(FoursquareUserInfo)
	flickr_user_info = EmbeddedDocumentField(FlickrUserInfo)
	facebook_user_info = EmbeddedDocumentField(FacebookUserInfo)
	khanacademy_user_info = EmbeddedDocumentField(KhanAcademyUserInfo)
	twitter_user_info = EmbeddedDocumentField(TwitterUserInfo)
	google_user_info = EmbeddedDocumentField(GoogleUserInfo)



class BodyMeasurements(EmbeddedDocument):
	date = StringField()
	user_id = StringField()
	weight = FloatField()
	bmi = FloatField()
	fat_mass = FloatField()
	lean_mass = FloatField()
	height = FloatField()
	bloodpressure = FloatField()
	heart_rate = FloatField()
	blood_glucose = FloatField()
	# sleep
	# nutrition
	# physicalActivity
	# location

################ FITIBIT ################
class ActivitiesDescription(EmbeddedDocument): # this needs to be looked into. 
	ftbt_activity_id = IntField()			   # what is the purpose of this?
	ftbt_activity_parent_id = IntField()	   # is it generic model of an activity type?
	ftbt_calories = IntField()
	ftbt_description = StringField()
	ftbt_distance = FloatField()
	ftbt_duration = IntField()
	ftbt_has_start_time = BooleanField()
	ftbt_is_favorite = BooleanField()
	ftbt_log_id = IntField()
	ftbt_name = StringField()
	ftbt_start_time = DateTimeField()
	ftbt_steps = IntField()

class FitbitActivitiesSummary(EmbeddedDocument):
	ftbt_activity_score = IntField()
	ftbt_activity_calories = IntField()
	ftbt_calories_out = IntField()
	ftbt_distance = ListField(FloatField())
	ftbt_elevation = FloatField()
	ftbt_floors = IntField()
	ftbt_mins_sedentary = IntField()
	ftbt_mins_lightly_active = IntField()
	ftbt_mins_fairly_active = IntField()
	ftbt_mins_very_active = IntField()
	ftbt_marginal_calories = IntField()
	ftbt_steps = IntField()

class FitbitActivity(EmbeddedDocument):
	date = StringField()
	user_id = StringField()
	type = StringField() # fitbit or other activity source (say, nike or )
	activity_description = EmbeddedDocumentField(ActivitiesDescription)
	activity_summary = EmbeddedDocumentField(FitbitActivitiesSummary)

class FitbitPhysicalActivity(Document):
	created_at = StringField()
	user_id = StringField()
	ftbt_steps = IntField()
	ftbt_distance = FloatField()
	ftbt_calories_out = IntField()
	ftbt_activity_calories = IntField()
	ftbt_floors = IntField()
	ftbt_elevation = FloatField()
	ftbt_mins_sedentary = IntField()
	ftbt_mins_lightly_active = IntField()
	ftbt_mins_fairly_active = IntField()
	ftbt_mins_very_active = IntField()
	ftbt_active_score = IntField()
	ftbt_activities = ListField(EmbeddedDocumentField(FitbitActivity))

class FitbitBodyData(Document):
	created_at = StringField()
	user_id = StringField()
	ftbt_weight = FloatField()
	ftbt_bmi = FloatField()
	ftbt_fat = FloatField()

class FitbitFoodUnit(EmbeddedDocument):
	ftbt_unit_id = IntField()
	ftbt_unit_name = StringField()
	ftbt_unit_plural = StringField()

class FitbitFood(Document):
	created_at = StringField() #needed?
	user_id = StringField()
	ftbt_amount = FloatField()
	ftbt_brand = StringField()
	ftbt_food_id = IntField()
	ftbt_meal_type_id = IntField()
	ftbt_unit = EmbeddedDocumentField(FitbitFoodUnit)
	ftbt_calories = IntField()
	ftbt_carbs = FloatField()
	ftbt_fat = FloatField()
	ftbt_fiber = FloatField()
	ftbt_protein = FloatField()
	ftbt_sodium = FloatField()
	ftbt_sugar = FloatField()
	ftbt_water = BooleanField()
	# image = ImageField()
	# location = GeoPointField()
	ftbt_name = StringField()
	# user_given_name = StringField()

class FitbitSleep(Document):
	created_at = StringField()
	user_id = StringField()
	ftbt_start_time = StringField()
	ftbt_time_in_bed = StringField
	ftbt_minutes_asleep = IntField()
	ftbt_awakenings_count = IntField()
	ftbt_minutes_awake = IntField()
	ftbt_minutes_to_fall_asleep = IntField()
	ftbt_minutes_after_wakeup = IntField()
	ftbt_efficiency = IntField()	


############# SLEEP ############# 
class ZeoDate(EmbeddedDocument):
	year = IntField()
	month = IntField()
	day = IntField()
	hour = IntField()

class ZeoSleep(Document):
	date = StringField()
	user_id = StringField()
	type = StringField() #zeo, fitbit, other
	awakenings = IntField()
	awakenings_zq_points = IntField()
	bed_time = DateTimeField()
	grouping = ListField() #find out what type this is?  docs say 'enum', so list?
	morning_feel = IntField()
	rise_time = DateTimeField()
	start_time = DateTimeField()
	time_in_deep = IntField()
	time_in_deep_percentage = IntField()
	time_in_deep_zq_points = IntField()
	time_in_light = IntField()
	time_in_light_perentage = IntField()
	time_in_light_zq_points = IntField()
	time_in_rem = IntField()
	time_in_rem_percentage = IntField()
	time_in_rem_zq_points = IntField()
	time_in_wake = IntField()
	time_in_wake_percentage = IntField()
	time_in_wake_zq_points = IntField()
	time_to_z = IntField()
	total_z = IntField()
	total_z_zq_points = IntField()
	zq = IntField()
	alarm_reason = StringField()
	alarm_ring_index = IntField()
	dayFeel = IntField()
	sleep_graph = ListField(StringField())
	sleep_graph_start_time = DateTimeField()
	sleep_stealer_score = IntField()
	wake_window_end_index = IntField() #? is this an int?
	wake_window_start_index = IntField() #? is this an int?


############# FOURSQUARE ############# 
class VenueStats(EmbeddedDocument):
	tip_count = IntField()
	checkins_count = IntField()
	users_field = IntField()


class VenueCategory(EmbeddedDocument):
	category_id = StringField()
	name = StringField()
	plural = StringField()
	short_name = StringField()
	primary = BooleanField()
	parents = ListField(StringField)


class VenueStats(EmbeddedDocument):
	checkins_count = IntField()
	users_count = IntField()
	tip_count = IntField()


class VenueLikesGroup(EmbeddedDocument):
	type = StringField()
	count = IntField()
	summary = StringField()
	# itmes = ListField() fs user-object 


class VenueBeenHere(EmbeddedDocument):
	count = IntField()
	marked = BooleanField()


class VenueLikes(EmbeddedDocument):
	count = IntField()
	groups = ListField(EmbeddedDocumentField(VenueLikesGroup))


class VenueMenu(EmbeddedDocument):
	url = StringField()
	mobile_url = StringField()
	type = StringField()


class CheckInLikes(EmbeddedDocument):
	type = StringField()
	count = IntField()
	summary = StringField()


class VenueContact(EmbeddedDocument):
	phone = StringField()
	formatted_phone = StringField()
	twitter = StringField()
	facebook = StringField()


class VenueLocation(EmbeddedDocument):
	address = StringField()
	cross_street = StringField()
	lat = FloatField()
	lng = FloatField()
	postal_code = StringField()
	city = StringField()
	state = StringField()
	country = StringField()
	cc = StringField()


class Venue(EmbeddedDocument):
	venue_id = StringField()
	name = StringField()
	contact = EmbeddedDocumentField(VenueContact)
	location = EmbeddedDocumentField(VenueLocation)
	cannonical_url = StringField()
	categories = ListField(EmbeddedDocumentField(VenueCategory))
	verified = BooleanField()
	stats = EmbeddedDocumentField(VenueStats)
	url = StringField()
	likes = EmbeddedDocumentField(VenueLikes)
	like = BooleanField()
	menu = EmbeddedDocumentField(VenueMenu)


class CheckIn(Document):
	record_created_at = DateTimeField
	user_id = StringField()
	fs_id = StringField()
	fs_created_at = IntField()
	fs_type = StringField()
	fs_timezone_offset = IntField()
	fs_timezone = StringField()
	fs_venue = EmbeddedDocumentField(Venue)
	fs_like = BooleanField()
	fs_likes = ListField(EmbeddedDocumentField(CheckInLikes))


############# EDUCATION ############# 
class KhanAcademyVideo(EmbeddedDocument):
	date_added = DateTimeField()
	description = StringField()
	duration = IntField()
	ka_url = StringField()
	keywords = StringField()
	kind = StringField()
	playlists = ListField()
	readable_id = StringField()
	title = StringField()
	url = StringField()
	views = IntField()
	youtube_id = StringField()

class KhanAcademyVideoLog(EmbeddedDocument):
	kind = StringField()
	playlist_titles = ListField()
	points_earned = IntField()
	seconds_watched = IntField()
	time_watched = DateTimeField()
	user = StringField()
	video_title = StringField()

class KhanAcademyUserExercise(EmbeddedDocument):
	exercise = StringField()
	first_done = DateTimeField()
	kind = StringField()
	last_done = DateTimeField()
	last_review = DateTimeField()
	longest_streak = IntField()
	proficient_date = StringField()
	seconds_per_fast_problem = FloatField()
	streak = IntField()
	summative = BooleanField()
	total_done = IntField()
	user = StringField() 

class KhanAcademyUserVideos(EmbeddedDocument):
	completed = BooleanField()
	duration = IntField()
	kind = StringField()
	last_second_watched = IntField()
	last_watched = DateTimeField()
	points = IntField()
	seconds_watched = IntField()
	user = StringField()
	videos = ListField(EmbeddedDocumentField(KhanAcademyVideo))
	video_logs = ListField(EmbeddedDocumentField(KhanAcademyVideoLog))
	exercises = ListField(EmbeddedDocumentField(KhanAcademyUserExercise))

class KhanAcademyStats(Document):
	date = StringField()
	user_id = StringField()
	all_proficient_exercises = ListField()
	badge_counts = ListField()
	coaches = ListField()
	joined = DateTimeField()
	last_activity = DateTimeField()
	nickname = StringField()
	points = IntField()
	proficient_exercises = ListField()
	suggested_exercises = ListField()
	total_seconds_watched = IntField()
	khan_academy_user_id = StringField()
	prettified_user_email = StringField()






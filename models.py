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


class Body(Document):
	date = DateTimeField()
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

############# PHYSICAL ACTIVITY ############# 
class ActivitiesDescription(EmbeddedDocument): # this needs to be looked into. 
	fitbit_activity_id = IntField()			   # what is the purpose of this?
	fitbit_activity_parent_id = IntField()	   # is it generic model of an activity type?
	calories = IntField()
	description = StringField()
	distance = FloatField()
	duration = IntField()
	has_start_time = BooleanField()
	is_favorite = BooleanField()
	log_id = IntField()
	name = StringField()
	start_time = DateTimeField()
	steps = IntField()

class ActivitiesSummary(EmbeddedDocument):
	fitbit_activity_score = IntField()
	fitbit_activity_calories = IntField()
	calories_out = IntField()
	distances = ListField(FloatField())
	elevation = FloatField()
	floors = IntField()
	mins_sedentary = IntField()
	mins_lightly_active = IntField()
	mins_fairly_active = IntField()
	mins_highly_active = IntField()
	marginal_calories = IntField()
	steps = IntField()

class Activity(EmbeddedDocument):
	date = DateTimeField()
	user_id = StringField()
	type = StringField() # fitbit or other activity source (say, nike or )
	activity_description = EmbeddedDocumentField(ActivitiesDescription)
	activity_summary = EmbeddedDocumentField(ActivitiesSummary)

class PhysicalActivity(Document):
	date = DateTimeField()
	user_id = StringField()
	steps = IntField()
	distance = FloatField()
	calories_out = IntField()
	activity_calories = IntField()
	floors = IntField()
	elevation = FloatField()
	mins_sedentary = IntField()
	mins_lightly_active = IntField()
	mins_moderately_active = IntField()
	mins_highly_active = IntField()
	active_score = IntField()
	activities = ListField(EmbeddedDocumentField(Activity))



############# NUTRITION ############# 
class FoodUnit(EmbeddedDocument):
	fitbit_unit_id = IntField()
	fitbit_unit_name = StringField()
	fitbit_unit_plural = StringField()

class Food(Document):
	date = DateTimeField() #needed?
	user_id = StringField()
	amount = FloatField()
	brand = StringField()
	fitbit_food_id = IntField()
	fitbit_mealy_type_id = IntField()
	unit = EmbeddedDocumentField(FoodUnit)
	calories = IntField()
	carbs = FloatField()
	fat = FloatField()
	fiber = FloatField()
	protein = FloatField()
	sodium = FloatField()
	sugar = FloatField()
	water = BooleanField()
	# image = ImageField()
	location = GeoPointField()
	fitbit_name = StringField()
	user_given_name = StringField()



############# SLEEP ############# 
class ZeoDate(EmbeddedDocument):
	year = IntField()
	month = IntField()
	day = IntField()
	hour = IntField()

class Sleep(Document):
	date = DateTimeField()
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


############# LOCATION ############# 
class VenueContact(EmbeddedDocument):
	phone = StringField()
	formattedPhone = StringField()
	twitter = StringField()
	facebook = StringField()


class VenueLocation(EmbeddedDocument):
	address = StringField()
	cross_street = StringField()
	location = GeoPointField()
	postal_code = StringField()
	city = StringField()
	state = StringField()
	country = StringField()
	cc = StringField()


class VenueCategory(EmbeddedDocument):
	name = StringField()
	plural = StringField()
	short_name = StringField()


class VenueStats(EmbeddedDocument):
	checkins_count = IntField()
	users_count = IntField()
	tip_count = IntField()


class Venue(EmbeddedDocument):
	foursqure_venue_id = StringField()
	name = StringField()
	contact = EmbeddedDocumentField(VenueContact)
	location = EmbeddedDocumentField(VenueLocation)
	categories = ListField(EmbeddedDocumentField(VenueCategory))
	stats = EmbeddedDocumentField(VenueStats)

class Location(Document):
	datetime = DateTimeField
	user_id = StringField()
	type = StringField() #foursquare or openpaths
	location = GeoPointField()
	venue = EmbeddedDocumentField(Venue)


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
	proficient_date = DateTimeField()
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
	date = DateTimeField()
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






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
	# sleep
	# nutrition
	# physicalActivity
	# location


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


class FoodUnit(EmbeddedDocument):
	fitbit_unit_id = IntField()
	fitbit_unit_name = StringField()
	fitbit_unit_plural = StringField()

class Food(Document):
	createdat = DateTimeField() #needed?
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


import os, sys

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

class Location(Document):
	phro_created_at = IntField()
	username = StringField()
	created_at = IntField()
	source = StringField() #foursquare, openpaths, flickr
	# source_id = ObjectIdField()
	loc = GeoPointField()
	alt = IntField()
	accuracy = IntField()
	venue_name = StringField()
	venue_category = StringField()
	address = StringField()
	cross_street = StringField()
	neighborhood = StringField()
	postal_code = StringField()
	city = StringField()
	locality = StringField()
	county = StringField()
	state = StringField()
	region = StringField()
	country = StringField()
	cc = StringField()

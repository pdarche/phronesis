import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

############# FOURSQUARE MODELS ############# 
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
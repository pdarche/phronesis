import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

############# FLICKR MODELS ############# 
class FlickrPhotoOwner(EmbeddedDocument):
	nsid = StringField()
	username = StringField()
	realname = StringField()
	location = StringField()
	iconserver = StringField()
	iconfarm = IntField()

class FlickrPhotoDescription(EmbeddedDocument):
	_content = StringField()

class FlickrPhotoVisibility(EmbeddedDocument):
	is_public = IntField()
	is_friend = IntField()
	is_family = IntField()

class FlickrPhotoDates(EmbeddedDocument):
	posted = StringField()
	taken = StringField()
	taken_granularity = IntField()
	last_update = StringField()

class FlickrPhotoPermissions(EmbeddedDocument):
	perm_comment = IntField()
	perm_add_meta = IntField()
	views = IntField()

class FlickrPhotoEditability(EmbeddedDocument):
	can_comment = IntField()
	can_meta_data = IntField()

class FlickrPhotoPublicEditability(EmbeddedDocument):
	can_comment = IntField()
	can_meta_data = IntField()

class FlickrPhotoUsage(EmbeddedDocument):
	can_download = IntField()
	can_blog = IntField()
	can_print = IntField()

class FlickrPhotoTags(EmbeddedDocument):
	tag_id = StringField()
	author = StringField()
	raw = StringField()
	_content = StringField()
	machine_tag = IntField()

class FlickrPhotoNote(EmbeddedDocument):
	note = StringField()

class FlickrPhotoPerson(EmbeddedDocument):
	has_people = IntField()

class FlickrPhotoUrl(EmbeddedDocument):
	type = StringField()
	_content = StringField

class FlickrPhotoLocation(EmbeddedDocument):
	lat = FloatField()
	lon = FloatField()
	accuracy = IntField()
	context = IntField()
	neightborhood = StringField()
	locality = StringField()
	county = StringField()
	region = StringField()


class FlickrPhotoInfo(EmbeddedDocument):
	photo_id = StringField()
	secret = StringField()
	server = StringField()
	farm = IntField()
	date_uploaded = StringField()
	is_favorite = IntField()
	license = IntField()
	safety_level = IntField()
	rotation = IntField()
	original_secret = StringField()
	original_format = StringField()
	owner = EmbeddedDocumentField(FlickrPhotoOwner)
	title = StringField()
	description = EmbeddedDocumentField(FlickrPhotoDescription)
	visibility = EmbeddedDocumentField(FlickrPhotoVisibility)
	dates = EmbeddedDocumentField(FlickrPhotoDates)
	permissions = EmbeddedDocumentField(FlickrPhotoPermissions)
	editability = EmbeddedDocumentField(FlickrPhotoEditability)
	public_editability = EmbeddedDocumentField(FlickrPhotoPublicEditability)
	usage = EmbeddedDocumentField(FlickrPhotoUsage)
	notes = ListField(EmbeddedDocumentField(FlickrPhotoNote))
	people = EmbeddedDocumentField(FlickrPhotoPerson)
	tags = ListField(EmbeddedDocumentField(FlickrPhotoNote))
	location = EmbeddedDocumentField(FlickrPhotoLocation)
	urls = EmbeddedDocumentField(FlickrPhotoUrl)

class FlickrPhoto(Document):
	phro_created_at = IntField()
	username = StringField()
	photo_id = StringField()
	owner = StringField()
	secret = StringField()
	server = StringField()
	farm = IntField()
	title = StringField()
	is_public = IntField()
	is_friend = IntField()
	is_family = IntField()
	has_geo = BooleanField()
	info = EmbeddedDocumentField(FlickrPhotoInfo)


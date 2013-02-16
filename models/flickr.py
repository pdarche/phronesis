import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

############# FLICKR MODELS ############# 
class FlickrPhoto(Document):
	record_created_at = StringField()
	user_id = StringField()
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

import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

############# OPEN PATHS MODELS ############# 
class OpenPathsLocation(Document):
	phro_created_at = IntField()
	username = StringField()
	device = StringField()
	os = StringField()
	t = IntField()
	lat = FloatField()
	lon = FloatField()
	alt = FloatField()
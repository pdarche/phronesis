import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

class Trigger(EmbeddedDocument):
	created_at = IntField()
	activation_time = IntField()
	location = GeoPointField()
	is_recurring = BooleanField()

class HabitInfo(EmbeddedDocument):
	url = StringField()
	actions = ListField()
	triggers = ListField(EmbeddedDocumentField(Trigger))

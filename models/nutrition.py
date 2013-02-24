import os, sys

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

class NutritionInfoField(Embedded)

class NutritionRecord(Document):
	phro_create_at = IntField()
	username = StringField()
	create_at = IntField()
	img_url = UrlField()
	name = StringField()
	venue = StringField()
	venue_category String()
	loc = GeopointField()
	nutrition_info = EmbeddedDocumentField(NutritionInfoField())
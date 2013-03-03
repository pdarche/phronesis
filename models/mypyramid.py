import os, sys

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

class MyPyramidReferenceInfo(Document):
	food_code = IntField()
	display_name = StringField()
	portion_default = FloatField()
	portion_amount = FloatField()
	portion_display_name = StringField()
	factor = FloatField()
	increment = FloatField()
	multiplier = FloatField()
	grains = FloatField()
	whole_grains = FloatField()
	vegetables = FloatField()
	orange_vegetables = FloatField()
	drkgreen_vegetables = FloatField()
	starchy_vegetables = FloatField()
	other_vegetables = FloatField()
	fruits = FloatField()
	milk = FloatField()
	meats = FloatField()
	soy = FloatField()
	drybeans_peas = FloatField()
	oils = FloatField()
	solid_fats = FloatField()
	added_sugars = FloatField()
	alcohol = FloatField()
	calories = FloatField()
	saturated_fats = FloatField()

	
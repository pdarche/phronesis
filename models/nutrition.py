import os, sys

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

class StandardLabelNutritionInfo(EmbeddedDocument)
	calories = FloatField()
	calories_from_fat = FloatField()
	total_fat = FloatField()
	saturated_fat = FloatField()
	trans_fat = FloatField()
	cholesterol = FloatField()
	sodium = FloatField()
	total_carbs = FloatField()
	dietary_fiber = FloatField()
	sugar = FloatField()
	protein = FloatField()
	vit_a = IntField()
	vit_c = IntField()
	calcium = IntField()
	iron = IntField()


class MyPyramidNutritionInfo(EmbeddedDocument)
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


class NutritionRecord(Document):
	phro_create_at = IntField()
	username = StringField()
	create_at = IntField()
	img_url = UrlField()
	name = StringField()
	pyramid_name = StringField()
	venue = StringField()
	venue_category String()
	loc = GeopointField()
	my_pyramid = EmbeddedDocumentField(MyPyramidNutritionInfo())
	standard_label = EmbeddedDocumentField(StandardLabelNutritionInfo())



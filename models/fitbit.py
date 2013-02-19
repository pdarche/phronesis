import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

################ FITIBIT MODELS ################
class ActivitiesDescription(EmbeddedDocument): # this needs to be looked into. 
	ftbt_activity_id = IntField()			   # what is the purpose of this?
	ftbt_activity_parent_id = IntField()	   # is it generic model of an activity type?
	ftbt_calories = IntField()
	ftbt_description = StringField()
	ftbt_distance = FloatField()
	ftbt_duration = IntField()
	ftbt_has_start_time = BooleanField()
	ftbt_is_favorite = BooleanField()
	ftbt_log_id = IntField()
	ftbt_name = StringField()
	ftbt_start_time = DateTimeField()
	ftbt_steps = IntField()

class FitbitActivitiesSummary(EmbeddedDocument):
	ftbt_activity_score = IntField()
	ftbt_activity_calories = IntField()
	ftbt_calories_out = IntField()
	ftbt_distance = ListField(FloatField())
	ftbt_elevation = FloatField()
	ftbt_floors = IntField()
	ftbt_mins_sedentary = IntField()
	ftbt_mins_lightly_active = IntField()
	ftbt_mins_fairly_active = IntField()
	ftbt_mins_very_active = IntField()
	ftbt_marginal_calories = IntField()
	ftbt_steps = IntField()

class FitbitActivity(EmbeddedDocument):
	date = StringField()
	user_id = StringField()
	activity_description = EmbeddedDocumentField(ActivitiesDescription)
	activity_summary = EmbeddedDocumentField(FitbitActivitiesSummary)

class FitbitPhysicalActivity(Document):
	created_at = StringField()
	user_id = StringField()
	ftbt_steps = IntField()
	ftbt_distance = FloatField()
	ftbt_calories_out = IntField()
	ftbt_activity_calories = IntField()
	ftbt_floors = IntField()
	ftbt_elevation = FloatField()
	ftbt_mins_sedentary = IntField()
	ftbt_mins_lightly_active = IntField()
	ftbt_mins_fairly_active = IntField()
	ftbt_mins_very_active = IntField()
	ftbt_active_score = IntField()
	ftbt_activities = ListField(EmbeddedDocumentField(FitbitActivity))

class FitbitBodyData(Document):
	created_at = StringField()
	user_id = StringField()
	ftbt_weight = FloatField()
	ftbt_bmi = FloatField()
	ftbt_fat = FloatField()

class FitbitFoodUnit(EmbeddedDocument):
	ftbt_unit_id = IntField()
	ftbt_unit_name = StringField()
	ftbt_unit_plural = StringField()

class FitbitFood(Document):
	created_at = StringField() #needed?
	user_id = StringField()
	ftbt_amount = FloatField()
	ftbt_brand = StringField()
	ftbt_food_id = IntField()
	ftbt_meal_type_id = IntField()
	ftbt_unit = EmbeddedDocumentField(FitbitFoodUnit)
	ftbt_calories = IntField()
	ftbt_carbs = FloatField()
	ftbt_fat = FloatField()
	ftbt_fiber = FloatField()
	ftbt_protein = FloatField()
	ftbt_sodium = FloatField()
	ftbt_sugar = FloatField()
	ftbt_water = BooleanField()
	# image = ImageField()
	# location = GeoPointField()
	ftbt_name = StringField()
	# user_given_name = StringField()

class FitbitSleep(Document):
	created_at = StringField()
	user_id = StringField()
	ftbt_start_time = StringField()
	ftbt_time_in_bed = StringField
	ftbt_minutes_asleep = IntField()
	ftbt_awakenings_count = IntField()
	ftbt_minutes_awake = IntField()
	ftbt_minutes_to_fall_asleep = IntField()
	ftbt_minutes_after_wakeup = IntField()
	ftbt_efficiency = IntField()	


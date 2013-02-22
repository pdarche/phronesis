import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

class IntraDayStep(EmbeddedDocument):
	level = IntField()
	time = StringField()
	value = FloatField()

class ActivityDescription(EmbeddedDocument):
	ftbt_activity_id = IntField()			   
	ftbt_activity_parent_id = IntField()	   
	calories = IntField()
	description = StringField()
	distance = FloatField()
	duration = IntField()
	has_start_time = BooleanField()
	is_favorite = BooleanField()
	log_id = IntField()
	name = StringField()
	start_time = DateTimeField()
	steps = IntField()

class ActivitySummary(EmbeddedDocument):
	activity_calories = IntField()
	calories_out = IntField()
	distance = ListField(FloatField())
	elevation = FloatField()
	floors = IntField()
	mins_sedentary = IntField()
	mins_lightly_active = IntField()
	mins_fairly_active = IntField()
	mins_very_active = IntField()
	marginal_calories = IntField()
	steps = IntField()

class Activty(EmbeddedDocument):
	activity_description = EmbeddedDocumentField(ActivityDescription)
	activity_summary = EmbeddedDocumentField(ActivitiesSummary)

class PhysicalActivity(Document)
	prho_created_at = IntField()
	username = StringField()
	source = ListFieled(StringField) #fitbit, nike+, etc
	source_id = ListFieled(ObjectIdField)x
	steps = IntField()
	distance = FloatField()
	calories_out = IntField()
	floors = IntField()
	mins_sedentary = IntField()
	mins_ligthly_active = IntField()
	mins_farily_active = IntField()
	mins_very_active = IntField()
	intra_day_stesp = ListField(EmbeddedDocumentField(IntraDayStep))
	activities = ListField(EmbeddedDocumentField(Activity))


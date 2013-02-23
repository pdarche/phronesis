import os, sys

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime


class DateTime(EmbeddedDocument):
	year = IntField()
	month = IntField()
	day = IntField()
	hour = IntField()
	minute = IntField()
	second = IntField()

class SleepRecord(Document):
	phro_create_at = IntField()
	username = StringField()
	start_date = EmbeddedDocumentField(DateTime)
	awakenings = IntField()
	bed_time = EmbeddedDocumentField(DateTime)
	grouping = StringField()
	morning_feel = IntField()
	rise_time = EmbeddedDocumentField(DateTime)
	time_in_deep = IntField()
	time_in_deep_percentage = IntField()
	time_in_deep_zq_points = IntField()
	time_in_light = IntField()
	time_in_light_perentage = IntField()
	time_in_rem = IntField()
	time_in_rem_percentage = IntField()
	time_in_rem_zq_points = IntField()
	time_in_wake = IntField()
	time_in_wake_percentage = IntField()
	time_in_wake_zq_points = IntField()
	time_to_z = IntField()
	total_z = IntField()
	total_z_zq_points = IntField()
	zq = IntField()
	alarm_reason = StringField()
	alarm_ring_index = IntField()
	dayFeel = IntField()
	sleep_graph = ListField()
	sleep_graph_start_time = EmbeddedDocumentField(DateTime)
	sleep_stealer_score = IntField()
	wake_window_end_index = IntField() #? is this an int?
	wake_window_start_index = IntField() #? is this an int?
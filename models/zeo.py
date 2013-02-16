import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

############# SLEEP ############# 
class ZeoDateTime(EmbeddedDocument):
	year = IntField()
	month = IntField()
	day = IntField()
	hour = IntField()
	minute = IntField()
	second = IntField()

class ZeoSleepRecord(Document):
	created_at = StringField()
	user_id = StringField()
	start_date = EmbeddedDocumentField(ZeoDateTime)
	awakenings = IntField()
	awakenings_zq_points = IntField()
	bed_time = EmbeddedDocumentField(ZeoDateTime)
	grouping = StringField() #find out what type this is?  docs say 'enum', so list?
	morning_feel = IntField()
	rise_time = EmbeddedDocumentField(ZeoDateTime)
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
	sleep_graph_start_time = EmbeddedDocumentField(ZeoDateTime)
	sleep_stealer_score = IntField()
	wake_window_end_index = IntField() #? is this an int?
	wake_window_start_index = IntField() #? is this an int?
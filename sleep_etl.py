import os 
import sys
import time

import models.zeo as zeo
import models.sleep as sleep

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

#python mongo hooks
from pymongo import MongoClient
import bson

connect('local_db')

#get all the zeo records that haven't been incorporated into sleep records 
def last_zeo():
	last_sleep = sleep.SleepRecord.objects(username="pdarche")

	if len(last_sleep) == 0:
		sleep_records = zeo.ZeoSleepRecord.objects(username="pdarche") 
		return sleep_records
	else:
		last_record = sleep.SleepRecord.objects(username="pdarche").order_by("-t")
		latest = last_record[0].phro_created_at
		new_records = zeo.ZeoSleepRecord.objects(t__gte=latest)

		if len(new_records) == 0:
			print "all updated"
		else:
			print "records to update"

def last_ftbt():
	last_sleep = sleep.SleepRecord.objects(username="pdarche")

	if len(last_sleep) == 0:
		sleep_records = fitbit.FitbitSleep.objects(username="pdarche")
		return sleep_records
	else:
		last_record = sleep.SleepRecord.objects(username="pdarche").order_by("-t")
		latest = last_record[0].phro_created_at
		new_records = fitbit.FitbitSleep.objects(t__gte=latest)

		if len(new_records) == 0:
			print "all updated"
		else:
			print "records to update"

#get all the fitbit sleep records that haven't been incorporated into sleep records 

#for each zeo compare its date to each fitbit record's date 
	#if the fitbit date matches and the sleep values are non-zero create a combined record
	#else if the fitbit values are zero just use the zeo info
	#else just use the fitbit

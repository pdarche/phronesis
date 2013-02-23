import os 
import sys
import time

import models.fitbit as fitbit
import models.physact as physact

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

#python mongo hooks
from pymongo import MongoClient
import bson

connect('local_db')

def last_ftbt():
	last_ftbt = physact.PhysicalActivity.objects(username="pdarche")

	if len(last_ftbt) == 0:
		ftbt_records = fitbit.FitbitPhysicalActivity.objects(username="pdarche") 
		return ftbt_records
	else:
		last_record = physact.PhysicalActivity.objects(username="pdarche").order_by("-t")
		latest = last_record[0].phro_created_at
		new_records = fitbit.FitbitPhysicalActivity.objects(t__gte=latest)

		if len(new_records) == 0:
			print "all updated"
		else:
			print "records to update"


phys_activities = last_ftbt()
if phys_activities != 0:
	for phys_activity in phys_activities:
		dt = datetime.strptime(phys_activity.created_at, '%Y-%m-%d')
		created_at = int(time.mktime(dt.timetuple()))

		ftbt_activities = []

		if(len(phys_activity.ftbt_activities) != 0):
			for act in phys_activity.ftbt_activities:
				ftbt_act = physact.Activity(
					created_at = act.created_at,
					activity_description = act.activity_description,
					activity_summary = act.activity_summary
				)

				ftbt_activities.push(ftbt_act)

		activity = physact.PhysicalActivity(
			phro_create_at = int(time.time()),
			username = "pdarche",
			created_at = created_at,
			source = [ "Fitbit" ],
			steps = phys_activity.ftbt_steps,
			distance = phys_activity.ftbt_distance,
			calories_out = phys_activity.ftbt_calories_out,
			floors = phys_activity.ftbt_floors,
			mins_sedentary = phys_activity.ftbt_mins_sedentary,
			mins_lightly_active = phys_activity.ftbt_mins_lightly_active,
			mins_fairly_active = phys_activity.ftbt_mins_fairly_active,
			mins_very_active = phys_activity.ftbt_mins_very_active,
			intra_day_steps = [],
			activities = ftbt_activities
		)  

		if activity.save():
			print "activity saved"
		else:
			print "activity not saved"


import os 
import sys
import time

import models.zeo as zeo
import models.fitbit as fitbit
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
	print "sleep records %s" % len(last_sleep)

	if len(last_sleep) == 0:
		sleep_records = zeo.ZeoSleepRecord.objects(username="pdarche") 
		return sleep_records
	else:
		last_record = sleep.SleepRecord.objects(username="pdarche").order_by("-phro_created_at")
		latest = last_record[0].phro_created_at
		new_records = zeo.ZeoSleepRecord.objects(phro_created_at__gte=latest)

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
		last_record = sleep.SleepRecord.objects(username="pdarche").order_by("-phro_created_at")
		latest = last_record[0].phro_created_at
		new_records = fitbit.FitbitSleep.objects(phro_created_at__gte=latest)

		if len(new_records) == 0:
			print "all updated"
		else:
			print "records to update"

#get all the fitbit sleep records that haven't been incorporated into sleep records 
zeo_records = last_zeo()
ftbt_records = last_ftbt()

print len(zeo_records)
print len(ftbt_records)

z = list(zeo_records)

f = []
for ftbt in ftbt_records:
	if ftbt.ftbt_minutes_asleep != 0:
		f.append(ftbt)

z_date, f_date = ([], [])

#sort zeo records
z.sort(key=lambda x: 
datetime.strptime("%s-%s-%s" % ( x['start_date'].year, 
	x['start_date'].month, x['start_date'].day), '%Y-%m-%d'))

#sort fitbit records
f.sort(key=lambda x: 
datetime.strptime( x['created_at'], '%Y-%m-%d'))

#crete lists with fitbit and zeo dates
for date in f:
	f_d = date.created_at.encode('utf-8')
	f_d = datetime.strptime( f_d, '%Y-%m-%d')
	f_date.append(f_d)

for date in z:
	z_d = "%s-%s-%s" % (date.start_date.year, 
		date.start_date.month, date.start_date.day)
	z_d = datetime.strptime( z_d, '%Y-%m-%d')
	z_date.append(z_d)

#get the unique dates in the combined list
unique_dates = list(set(z_date + f_date))
#sort the unique dates
unique_dates.sort()

p0, p1 = (0,0)

def iterator(n):	
	for it in range(n):
		yield (p0,p1)

fin_list = []
for i,p in enumerate(iterator(len(unique_dates))):
	if p[0] != len(zeo_records):
		z_d = "%s-%s-%s" % (z[p[0]].start_date.year, # DANGER : THIS MAY BE WRONG
			z[p[0]].start_date.month, z[p[0]].start_date.day)
		z_date = datetime.strptime(z_d, '%Y-%m-%d')
	
	f_date = datetime.strptime(f[p[1]].created_at, '%Y-%m-%d')
	if z_date == f_date:
		new_record = { "date" : unique_dates[i], "zeo" : z[p[0]], "fitbit" : f[p[1]] }
		fin_list.append(new_record)
		p0 += 1
		p1 += 1

	elif z_date < f_date:
		new_record = { "date" : unique_dates[i], "zeo" : z[p[0]], "fitbit" : None }
		fin_list.append(new_record)
		if p0 != len(zeo_records) - 1:
			p0 += 1

	elif z_date > f_date:
		new_record = { "date" : unique_dates[i], "zeo" : None, "fitbit" : f[p[1]] }
		fin_list.append(new_record)
		if p1 != len(f) - 1:
			p1 += 1
		else:
			print "switchin over"
			new_record = { "date" : unique_dates[i], "zeo" : z[p[0]], "fitbit" : None }
			fin_list.append(new_record)
			if p0 != len(zeo_records) - 1: #DANGER : REEVALUATE THIS
				p0 += 1

	print p0, p1

for el in fin_list:
	if el["fitbit"] != None and el["zeo"] != None:
		z = el["zeo"]
		f = el["fitbit"]
		start_date_s = "%s-%s-%s" % (z.start_date.year, z.start_date.month, z.start_date.day)		

		start_date = sleep.DateTime(
				year = z.start_date.year,
				month = z.start_date.month,
				day = z.start_date.day,
				hour = z.start_date.hour,
				minute = z.start_date.minute,
				second = z.start_date.second
			)

		bed_time = sleep.DateTime(
				year = z.bed_time.year,
				month = z.bed_time.month,
				day = z.bed_time.day,
				hour = z.bed_time.hour,
				minute = z.bed_time.minute,
				second = z.bed_time.second
			)

		rise_time = sleep.DateTime(
				year = z.rise_time.year,
				month = z.rise_time.month,
				day = z.rise_time.day,
				hour = z.rise_time.hour,
				minute = z.rise_time.minute,
				second = z.rise_time.second
			)

		sleep_graph_start_time = sleep.DateTime(
				year = z.sleep_graph_start_time.year,
				month = z.sleep_graph_start_time.month,
				day = z.sleep_graph_start_time.day,
				hour = z.sleep_graph_start_time.hour,
				minute = z.sleep_graph_start_time.minute,
				second = z.sleep_graph_start_time.second
			)

		sleep_record = sleep.SleepRecord(
				phro_created_at = int(time.time()),
				username = "pdarche",
				source = ["Zeo", "Fitbit"],
				created_at = int(time.mktime(time.strptime(start_date_s, '%Y-%m-%d'))),
				start_date = start_date,
				awakenings = int(round((z.awakenings + f.ftbt_awakenings_count)/2)),
				bed_time = bed_time,
				grouping = z.grouping,
				morning_feel = z.morning_feel,
				rise_time = rise_time,
				time_in_deep = z.time_in_deep,
				time_in_deep_percentage = z.time_in_deep_percentage,
				time_in_deep_zq_points = z.time_in_deep_zq_points,
				time_in_light = z.time_in_light,
				time_in_light_percentage = z.time_in_light_percentage,
				time_in_rem = z.time_in_rem,
				time_in_rem_percentage = z.time_in_rem_percentage,
				time_in_rem_zq_points = z.time_in_rem_zq_points,
				time_in_wake = z.time_in_wake,
				time_in_wake_percentage = z.time_in_wake_percentage,
				time_in_wake_zq_points = z.time_in_wake_zq_points,
				time_to_z = z.time_to_z,
				total_z = z.total_z,
				total_z_zq_points = z.total_z_zq_points,
				zq = z.zq,
				alarm_reason = z.alarm_reason,
				day_feel = z.day_feel,
				sleep_graph = z.sleep_graph,
				sleep_graph_start_time = sleep_graph_start_time,
				sleep_stealer_score  = z.sleep_stealer_score,
				wake_window_end_index = z.wake_window_end_index,
				wake_window_start_index = z.wake_window_start_index
			)

		if sleep_record.save():
			print "zeo fitbit saved"
		else:
			print "not saved"
		# z = el["zeo"]
		# print "%s, fitbit %s, zeo %s" % (el["date"], el["fitbit"].created_at, 
		# 				"%s-%s-%s" % (z.start_date.year, z.start_date.month, z.start_date.day))
	
	elif el["fitbit"] != None:
		f = el["fitbit"]
		start_date_s = f.created_at.split('-')
		year = start_date_s[0]
		month = start_date_s[1]
		day = start_date_s[2]
		# t = datetime.strptime(f.ftbt_start_time, 
		# 					"%H:%M").strftime('%I:%M').lower().split(':')
		t = f.ftbt_start_time.split(":")
		hour = t[0]
		minute = t[1]
		
		start_date = sleep.DateTime(
				year = year,
				month = month,
				day = day,
				hour = None,
				minute = None,
				second = None
			)

		bed_time = sleep.DateTime(
				year = year,
				month = month,
				day = day,
				hour = hour,
				minute = minute,
				second = None
			)

		sleep_record = sleep.SleepRecord(
				phro_created_at = int(time.time()),
				username = "pdarche",
				source = ["Fitbit"],
				created_at = int(time.mktime(time.strptime(f.created_at, '%Y-%m-%d'))),
				start_date = start_date,
				awakenings = f.ftbt_awakenings_count,
				bed_time = bed_time,
				grouping = None,
				morning_feel = None,
				rise_time = None,
				time_in_deep = None,
				time_in_deep_percentage = None,
				time_in_deep_zq_points = None,
				time_in_light = None,
				time_in_light_percentage = None,
				time_in_rem = None,
				time_in_rem_percentage = None,
				time_in_rem_zq_points = None,
				time_in_wake = f.ftbt_minutes_awake,
				time_in_wake_percentage = int(round(f.ftbt_minutes_awake/f.ftbt_minutes_asleep)),
				time_in_wake_zq_points = None,
				time_to_z = f.ftbt_minutes_to_fall_asleep,
				total_z = f.ftbt_minutes_asleep,
				total_z_zq_points = None,
				zq = None,
				alarm_reason = None,
				day_feel = None,
				sleep_graph = None,
				sleep_graph_start_time = None,
				sleep_stealer_score  = None,
				wake_window_end_index = None,
				wake_window_start_index = None
			)
	
		if sleep_record.save():
			print "fitbit saved"
		else:
			print "not saved"

		# print "%s, fitbit: %s" % (el["date"], el["fitbit"].created_at)
	
	elif el["zeo"] != None:
		z = el["zeo"]
		start_date_s = "%s-%s-%s" % (z.start_date.year, z.start_date.month, z.start_date.day)

		start_date = sleep.DateTime(
				year = z.start_date.year,
				month = z.start_date.month,
				day = z.start_date.day,
				hour = z.start_date.hour,
				minute = z.start_date.minute,
				second = z.start_date.second
			)

		bed_time = sleep.DateTime(
				year = z.bed_time.year,
				month = z.bed_time.month,
				day = z.bed_time.day,
				hour = z.bed_time.hour,
				minute = z.bed_time.minute,
				second = z.bed_time.second
			)

		rise_time = sleep.DateTime(
				year = z.rise_time.year,
				month = z.rise_time.month,
				day = z.rise_time.day,
				hour = z.rise_time.hour,
				minute = z.rise_time.minute,
				second = z.rise_time.second
			)

		sleep_graph_start_time = sleep.DateTime(
				year = z.sleep_graph_start_time.year,
				month = z.sleep_graph_start_time.month,
				day = z.sleep_graph_start_time.day,
				hour = z.sleep_graph_start_time.hour,
				minute = z.sleep_graph_start_time.minute,
				second = z.sleep_graph_start_time.second
			)

		sleep_record = sleep.SleepRecord(
				phro_created_at = int(time.time()),
				username = "pdarche",
				source = ["Zeo", "Fitbit"],
				created_at = int(time.mktime(time.strptime(start_date_s, '%Y-%m-%d'))),
				start_date = start_date,
				awakenings = int(round((z.awakenings + f.ftbt_awakenings_count)/2)),
				bed_time = bed_time,
				grouping = z.grouping,
				morning_feel = z.morning_feel,
				rise_time = rise_time,
				time_in_deep = z.time_in_deep,
				time_in_deep_percentage = z.time_in_deep_percentage,
				time_in_deep_zq_points = z.time_in_deep_zq_points,
				time_in_light = z.time_in_light,
				time_in_light_percentage = z.time_in_light_percentage,
				time_in_rem = z.time_in_rem,
				time_in_rem_percentage = z.time_in_rem_percentage,
				time_in_rem_zq_points = z.time_in_rem_zq_points,
				time_in_wake = z.time_in_wake,
				time_in_wake_percentage = z.time_in_wake_percentage,
				time_in_wake_zq_points = z.time_in_wake_zq_points,
				time_to_z = z.time_to_z,
				total_z = z.total_z,
				total_z_zq_points = z.total_z_zq_points,
				zq = z.zq,
				alarm_reason = z.alarm_reason,
				day_feel = z.day_feel,
				sleep_graph = z.sleep_graph,
				sleep_graph_start_time = sleep_graph_start_time,
				sleep_stealer_score  = z.sleep_stealer_score,
				wake_window_end_index = z.wake_window_end_index,
				wake_window_start_index = z.wake_window_start_index
			)

		if sleep_record.save():
			print "zeo saved"
		else:
			print "not saved"
		
		# z = el["zeo"]
		# print "%s, zeo: %s" % (el["date"], "%s-%s-%s" % (z.start_date.year, 
		# 		z.start_date.month, z.start_date.day))


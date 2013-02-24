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
	z_d = "%s-%s-%s" % (z[p[0]].start_date.year, 
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
		if p0 != len(f) - 1:
			p0 += 1

	elif z_date > f_date:
		new_record = { "date" : unique_dates[i], "zeo" : None, "fitbit" : f[p[1]] }
		fin_list.append(new_record)
		if p1 != len(z) - 1:
			p1 += 1

for el in fin_list:
	if el["fitbit"] != None and el["zeo"] != None:
		z = el["zeo"]
		print "%s, fitbit %s, zeo %s" % (el["date"], el["fitbit"].created_at, 
						"%s-%s-%s" % (z.start_date.year, z.start_date.month, z.start_date.day))
	elif el["fitbit"] != None:
		print "%s, fitbit: %s" % (el["date"], el["fitbit"].created_at)
	elif el["zeo"] != None:
		z = el["zeo"]
		print "%s, zeo: %s" % (el["date"], "%s-%s-%s" % (z.start_date.year, 
				z.start_date.month, z.start_date.day))


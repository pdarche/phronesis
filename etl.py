import os 
import sys
import time

import models.openpaths as openpaths
import models.foursquare as foursquare
import models.location as location

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

#python mongo hooks
from pymongo import MongoClient
import bson

connect('local_db')

def last_op():
	last_op = location.Location.objects(source="Open Paths", username="pdarche")
	
	if len(last_op) == 0:
		op_locations = openpaths.OpenPathsLocation.objects(username="pdarche") 
		return op_locations
	else:
		last_record = openpaths.OpenPathsLocation.objects(username="pdarche").order_by("-t")
		latest = last_record[0].t
		new_records = openpaths.OpenPathsLocation.objects(t__gte=latest)
		
		if len(new_records) == 0:
			print "all updated"
		else:
			print "records to update"


def last_fs():
	last_fs = location.Location.objects(source="Foursquare")

	if len(last_fs) == 0:
		fs_checkins = foursquare.CheckIn.objects(username="pdarche")
		return fs_checkins
	else:
		last_record = foursquare.CheckIn.objects(username="pdarche").order_by("-t")
		latest = last_record[0].fs_created_at
		new_records = foursquare.CheckIn.objects(fs_created_at__gte=latest)
		
		if len(new_records) == 0:
			print "all updated"
		else:
			print "records to update"


#check for phro_created_at time for the last raw record
checkins = last_fs()
if checkins != None:
	for checkin in checkins:
		loc = location.Location(
			phro_created_at = int(time.time()),
			username = "pdarche",
			create_at = checkin.fs_created_at,
			source = "Foursquare",
			# source_id = checkin.id,
			lat = checkin.fs_venue.location.lat,
			lon = checkin.fs_venue.location.lng,
			alt = None,
			accuracy = None,
			venue_name = checkin.fs_venue.name,
			address = checkin.fs_venue.location.address,
			cross_street = checkin.fs_venue.location.cross_street,
			neighborhood = None,
			postal_code = checkin.fs_venue.location.postal_code,
			city = checkin.fs_venue.location.city,
			locality = None,
			county = None,
			state = checkin.fs_venue.location.state,
			country = checkin.fs_venue.location.country,
			cc = None
		)

		if loc.save():
			print "location saved",
		else:
			print "location not saved"

op_locations = last_op()
if op_locations != None:	
	for op_location in op_locations:
		loc = location.Location(
			phro_created_at = int(time.time()),
			username = "pdarche",
			create_at = op_location.t,
			source = "Open Paths",
			# source_id = op_location.null,
			lat = op_location.lat,
			lon = op_location.lon,
			alt = op_location.alt,
			accuracy = None,
			venue_name = None,
			address = None,
			cross_street = None,
			neighborhood = None,
			postal_code = None,
			city = None,
			locality = None,
			county = None,
			state = None,
			country = None,
			cc = None
		)

		if loc.save():
			print "location saved",
		else:
			print "location not saved"


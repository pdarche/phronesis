import os 
import sys
import time

import models.openpaths as openpaths
import models.foursquare as foursquare
import models.flickr as flickr
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

def last_flkr():
	last_flkr = location.Location.objects(source="Flickr")
	
	if len(last_flkr) == 0:
		flkr_locations = flickr.FlickrPhoto.objects(username="pdarche") 
		return flkr_locations
	else:
		last_record = flickr.FlickrPhoto.objects(username="pdarche").order_by("-phro_created_at")
		latest = last_record[0].info.date_uploaded
		new_records = flickr.FlickrPhoto.objects(phro_created_at__gte=latest)
		
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
			created_at = checkin.fs_created_at,
			source = "Foursquare",
			# source_id = checkin.id,
			loc = [checkin.fs_venue.location.lng, checkin.fs_venue.location.lat],
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
			created_at = op_location.t,
			source = "Open Paths",
			# source_id = op_location.null,
			loc = [op_location.lon, op_location.lat],
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

flkr_locations = last_flkr()
if flkr_locations != None:
	for flkr_location in flkr_locations:
		if 	flkr_location.info.location != None:
			loc = location.Location(
				phro_created_at = int(time.time()),
				username = "pdarche",
				created_at = int(flkr_location.info.date_uploaded),
				source = "Flickr",
				# source_id = op_location.null,
				loc = [flkr_location.info.location.lon, flkr_location.info.location.lat],
				alt = None,
				accuracy = flkr_location.info.location.accuracy,
				venue_name = None,
				address = None,
				cross_street = None,
				neighborhood = flkr_location.info.location.neighborhood,
				postal_code = None,
				city = None,
				locality = flkr_location.info.location.locality,
				county = flkr_location.info.location.county,
				state = flkr_location.info.location.region,
				country = None,
				cc = None
			)

			if loc.save():
				print "location saved",
			else:
				print "location not saved"
				
		# if 	flkr_location.info.location != None:
		# 	print "location obj: %s lat: %s lon: %s" % (flkr_location.info.location,
		# 									flkr_location.info.location.lat,flkr_location.info.location.lon) 

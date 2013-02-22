import os 
import sys
import time

from models import openpaths
from models import location

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime


last_fs = location.Location.objects(source="Fourquare").order_by("-phro_created_at").limit(1)
last_op = location.Location.objects(source="Open Paths").order_by("-phro_created_at").limit(1)
# last_op = models.location.Location.first(source="Flickr")


#get the raw records for the user
# checkins = models.foursquare.CheckIn.objects(user_id=self.get_secure_cookie("username"))
# op_locations = models.openpaths.OpenPathLocation.objects((user_id=self.get_secure_cookie("username")))
# flickr_photos = models.flickr.FlickrPhoto.objects(user_id=self.get_secure_cookie("username"))

print last_op.create_at

#check for phro_created_at time for the last raw record

# for checkin in checkins:
# 	location = models.location.Location(
# 		phro_created_at = int(time.time()),
# 		username = self.get_secure_cookie("username"),
# 		create_at = checkin.fs_create_at,
# 		source = "Foursquare",
# 		source_id = checkin.id,
# 		lat = checkin.fs_venue.location.lat,
# 		lon = checkin.fs_venue.location.lng,
# 		alt = None,
# 		accuracy = None,
# 		venue_name = checkin.fs_venue.name,
# 		address = checkin.fs_venue.location.address,
# 		cross_street = checkin.fs_venue.location.cross_street,
# 		neighborhood = None,
# 		postal_code = checkin.fs_venue.location.postal_code,
# 		city = checkin.fs_venue.location.city,
# 		locality = None,
# 		county = None,
# 		state = checkin.fs_venue.location.state,
# 		country = checkin.fs_venue.location.country,
# 		cc = None
# 	)

# 	if location.save():
# 		print "location saved",
# 	else:
# 		print "location not saved"

# for op_location in op_locations:
# 	location = models.location.Location(
# 		phro_created_at = int(time.time()),
# 		username = self.get_secure_cookie("username"),
# 		create_at = op_location.t,
# 		source = "Open Paths",
# 		source_id = op_location.id,
# 		lat = op_location.lat,
# 		lon = op_location.location.lon,
# 		alt = op_location.alt,
# 		accuracy = None,
# 		venue_name = None,
# 		address = None,
# 		cross_street = None,
# 		neighborhood = None,
# 		postal_code = None,
# 		city = None,
# 		locality = None,
# 		county = None,
# 		state = None,
# 		country = None,
# 		cc = None
# 	)

# 	if location.save():
# 		print "location saved",
# 	else:
# 		print "location not saved"

# for op_location in op_locations:
# 	location = models.location.Location(
# 		phro_created_at = int(time.time()),
# 		username = self.get_secure_cookie("username"),
# 		create_at = op_location.t,
# 		source = "Open Paths",
# 		source_id = op_location.id,
# 		lat = op_location.lat,
# 		lon = op_location.location.lon,
# 		alt = op_location.alt,
# 		accuracy = None,
# 		venue_name = None,
# 		address = None,
# 		cross_street = None,
# 		neighborhood = None,
# 		postal_code = None,
# 		city = None,
# 		locality = None,
# 		county = None,
# 		state = None,
# 		country = None,
# 		cc = None
# 	)

# 	if location.save():
# 		print "location saved",
# 	else:
# 		print "location not saved"

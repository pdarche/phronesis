#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

import logging

class AppSettings(Document):
	fitbit_consumer_key = StringField()
	fitbit_consumer_secret = StringField()
	twitter_consumer_key = StringField()
	twitter_consumer_secret = StringField()
	facebook_api_key = StringField()
	facebook_secret = StringField()
	zeo_consumer_key = StringField()
	zeo_consumer_secret = StringField()
	foursquare_api_key = StringField()
	foursquare_client_id = StringField()
	foursquare_client_secret = StringField()
	google_consumer_key = StringField()
	google_consumer_secret = StringField()
	flickr_consumer_key = StringField()
	flickr_consumer_secret = StringField()
	khanacademy_consumer_key = StringField()
	khanacademy_consumer_secret = StringField()
	cookie_secret = StringField()

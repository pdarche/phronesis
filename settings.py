#mongo and models
from mongoengine import *
import models

#python mongo hooks
from pymongo import MongoClient
import bson

import inspect

#mongo connection
connect('local_db')

app_settings = models.AppSettings(
	fitbit_consumer_key = '8f5e05187b294f0989eb8cb9b20de54c',
	fitbit_consumer_secret = '0f88f60eae0142b586340594249e5f67',
	twitter_consumer_key = 'OaqpkBvltogUUjmeCqVhVw',
	twitter_consumer_secret = '0f88f60eae0142b586340594249e5f67',
	facebook_api_key = '426446497428837',
	facebook_secret = '7a811496573b875c107d3bafc1828cc2',
	zeo_consumer_key = 'peter.darche',
	zeo_consumer_secret = 'Aiy0EeXeRae9AebilaiK1t',
	foursquare_api_key = 'MSJXJGSMPMWVEEZKGCF1YEHUIAZG5YW3U4U0CNRZJYJ5TPPC',
	foursquare_client_id = 'MSJXJGSMPMWVEEZKGCF1YEHUIAZG5YW3U4U0CNRZJYJ5TPPC',
	foursquare_client_secret = '2CU20YV4WTEYKVQNKCXM51IMFDALG2RSLAHI5LGGMW0FSGBL',
	google_consumer_key = 'anonymous',
	google_consumer_secret = 'anonymous',
	flickr_consumer_key = '89e19ea49458a66cf9aa8c980e898655',
	flickr_consumer_secret = '03656cf0a41a75e1',
	khanacademy_consumer_key = 'ypzzb7hyX2Q9mVHR',
	khanacademy_consumer_secret = 'pfGvSc5adwCRCyE3',
	cookie_secret = 'NTliOTY5NzJkYTVlMTU0OTAwMTdlNjgzMTA5M2U3OGQ5NDIxZmU3Mg=='
)

# if app_settings.save():
# 	print "saved"
# else:
# 	print "you f'd up"

	
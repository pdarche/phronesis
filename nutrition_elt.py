import tornado.web
import tornado.auth
import tornado.gen
import tornado.httpclient

import os 
import sys
import time
import urllib
import json

import models.flickr as flickr
import models.userinfo as userinfo
import mixins.mixins as mixins

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

#python mongo hooks
from pymongo import MongoClient
import bson

connect('local_db')

def build_oauth_header(params):
    return "OAuth " + ", ".join(
            ['%s="%s"' % (k, urllib.quote(v)) for k, v in params.iteritems()])

class FlickrRequest(tornado.web.RequestHandler, tornado.auth.OAuthMixin):
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		user = userinfo.User.objects(username="pdarche")[0]
		photo = flickr.FlickrPhoto.objects(username="pdarche")[0]		
		# http = tornado.httpclient.AsyncHTTPClient()
		http = self.get_auth_http_client()
		oauth = self.return_oauth(
				api_key="89e19ea49458a66cf9aa8c980e898655",
				format="json",
				nojsoncallback="1", 
				method="flickr.photos.getInfo",
				photo_id=photo.photo_id,
				access_token=user.flickr_user_info.flickr_access_token,
			)

		response = yield tornado.gen.Task( http.fetch,
							oauth["url"],
							headers = {"authorization" : oauth["headers"] }
						)

		self.write(response.body)
		self.finish()

	def return_oauth(self, access_token=None, post_args=None, **args):
		""" make oauth authenticated requests without callbacks"""
		url_elems = []
		url_elems.append("http://api.flickr.com/services/rest/?")
		url_elems.append("&".join("%s=%s" % (k, str(v)) for k, v in sorted(args.items())))             
		url = "&".join(e for e in url_elems)

		# Add the OAuth resource request signature if web have credentials
		if access_token:
		    all_args = dict()
		    all_args.update(args)
		    if post_args is not None:
		        all_args.update(post_args)
		    method = "POST" if post_args is not None else "GET"            
		    oauth = self._oauth_request_parameters(
				url, access_token, all_args, method=method)
		
		params = { "url" : url, "headers" : build_oauth_header(oauth) }
		return params

	def _oauth_consumer_token(self):
		return {
		    'key': "89e19ea49458a66cf9aa8c980e898655",
		    'secret': "03656cf0a41a75e1"
		}

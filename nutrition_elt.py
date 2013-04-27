import tornado.web
import tornado.auth
import tornado.gen
import tornado.httpclient

import os 
import sys
import time
import urllib
import json
import ast

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
		photos = flickr.FlickrPhoto.objects(username="pdarche")
		for photo in photos:
			if photo.info == None:	
				http = self.get_auth_http_client()
				oauth = self.return_oauth(
						api_key=self.settings["flickr_consumer_key"],
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

				res = json.loads(response.body)
				# res = ast.literal_eval(response.body)

				owner = flickr.FlickrPhotoOwner(
						nsid = res["photo"]["owner"]["nsid"],
						username = res["photo"]["owner"]["username"],
						realname = res["photo"]["owner"]["realname"],
						location = res["photo"]["owner"]["location"],
						iconserver = res["photo"]["owner"]["iconserver"],
						iconfarm = res["photo"]["owner"]["iconfarm"]
					)

				description = flickr.FlickrPhotoDescription(
						_content = res["photo"]["description"]["_content"]
					)

				visibility = flickr.FlickrPhotoVisibility(
						is_public = res["photo"]["visibility"]["ispublic"],
						is_friend = res["photo"]["visibility"]["isfriend"],
						is_family = res["photo"]["visibility"]["isfamily"]
					)

				dates = flickr.FlickrPhotoDates(
						posted = res["photo"]["dates"]["posted"],
						taken = res["photo"]["dates"]["taken"],
						taken_granularity = res["photo"]["dates"]["takengranularity"],
						last_update = res["photo"]["dates"]["lastupdate"]
					)

				permissions = flickr.FlickrPhotoPermissions(
						perm_comment = res["photo"]["permissions"]["permcomment"],
						perm_add_meta = res["photo"]["permissions"]["permaddmeta"]
					)

				editability = flickr.FlickrPhotoEditability(
						can_comment = res["photo"]["editability"]["cancomment"],
						can_meta_data = res["photo"]["editability"]["canaddmeta"]
					)

				public_editability = flickr.FlickrPhotoPublicEditability(
						can_comment = res["photo"]["editability"]["cancomment"],
						can_meta_data = res["photo"]["editability"]["canaddmeta"]
					)

				usage = flickr.FlickrPhotoUsage(
						can_download = res["photo"]["usage"]["candownload"],
						can_blog = res["photo"]["usage"]["canblog"],
						can_print = res["photo"]["usage"]["canprint"]
					)

				# tags = flickr.PhotoTags()

				url = flickr.FlickrPhotoUrl(
						type = res["photo"]["urls"]["url"][0]["type"],
						_content = res["photo"]["urls"]["url"][0]["_content"]
					)

				if "location" in res["photo"].keys():		
					location = flickr.FlickrPhotoLocation(
							lat = res["photo"]["location"]["latitude"] if "latitude" in res["photo"]["location"].keys() else None,
							lon = res["photo"]["location"]["longitude"] if "longitude" in res["photo"]["location"].keys() else None,
							accuracy = res["photo"]["location"]["accuracy"] if "accuracy" in res["photo"]["location"].keys() else None,
							context = res["photo"]["location"]["context"] if "context" in res["photo"]["location"].keys() else None,
							neighborhood = res["photo"]["location"]["neighbourhood"]["_content"] if "neighbourhood" in res["photo"]["location"].keys() else None,
							locality = res["photo"]["location"]["locality"]["_content"] if "locality" in res["photo"]["location"].keys() else None,
							country = res["photo"]["location"]["country"]["_content"] if "country" in res["photo"]["location"].keys() else None,
							region = res["photo"]["location"]["region"]["_content"] if "region" in res["photo"]["location"].keys() else None
						)
				else:
					location = None

				photo_info = flickr.FlickrPhotoInfo(
						photo_id = res["photo"]["id"],
						secret = res["photo"]["secret"],
						server = res["photo"]["server"],
						farm = res["photo"]["farm"],
						date_uploaded = res["photo"]["dateuploaded"],
						is_favorite = res["photo"]["isfavorite"],
						license = res["photo"]["license"],
						safety_level = res["photo"]["safety_level"],
						rotation = res["photo"]["rotation"],
						original_secret = res["photo"]["originalsecret"],
						original_format = res["photo"]["originalformat"],
						owner = owner,
						title = res["photo"]["title"]["_content"],
						description = description,
						visibility = visibility,
						dates = dates,
						permissions = permissions,
						editability = editability,
						public_editability = public_editability,
						usage = usage,
						notes = None,
						people = None,
						tages = None,
						location = location,
						urls = url
					)

				photo.update(set__info=photo_info)
				self.write("success")
				print "updated"
		
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
		self.require_setting("flickr_consumer_key", "Flickr OAuth")
		self.require_setting("flickr_consumer_secret", "Flickr OAuth")
		return {
		    'key': self.settings["flickr_consumer_key"],
		    'secret': self.settings["flickr_consumer_secret"]
		}









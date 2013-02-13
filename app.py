#!/usr/bin/env python
# -*- coding: utf8 -*- 
import tornado.web
import tornado.httpserver 
import tornado.ioloop 
import tornado.options
import os.path
from tornado.options import define, options

#handlers
import handlers as h

#mongo and models
from mongoengine import *
import models

#python mongo hooks
from pymongo import MongoClient
import bson

define("port", default=8000, help="run on the given port", type=int)

#mongo connection
connect('local_db')

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", h.MainHandler),(r"/signup", h.SignUpHandler),
			(r"/login", h.LoginHandler),(r"/v1/users/(\w+)", h.UserInfoHandler),
			(r"/remove", h.RemoveUserHandler),
			(r"/docs", h.DocumentationHandler),
			(r"/v1/connect/twitter", h.TwitterConnectHandler),
			(r"/v1/connect/facebook", h.FacebookConnectHandler),
			(r"/v1/fitbit", h.FitbitConnectHandler),
			(r"/zeo", h.ZeoHandler),
			(r"/v1/zeobasic", h.ZeoBasicAuth),
			(r"/v1/foursquare", h.FoursquareHandler),
			(r"/v1/google", h.GoogleHandler),
			(r"/v1/flickr", h.FlickrHandler),
			(r"/v1/khanacademy", h.KhanAcademyHandler),
			(r"/v1/openpaths", h.OpenPathsHandler),
			(r"/v1/import/fitbit", h.FitbitImportHandler),
			(r"/v1/import/foursquare", h.FoursquareImportHandler),
			(r"/v1/import/openpaths", h.OpenPathsImportHandler),
			(r"/v1/import/flickr", h.FlickrImportHandler),
			(r"/v1/dumps/fitbit", h.FitbitDumpsHandler),
			(r"/v1/dumps/foursquare", h.FoursquareDumpsHandler),
			(r"/v1/dumps/openpaths", h.OpenPathsDumpsHandler),
			(r"/v1/dumps/flickr", h.FlickrDumpsHandler),
			(r"/v1/dumps/zeo", h.ZeoDumpsHandler),
			(r"/v1/remove/fitbit", h.RemoveUserFitbitHandler),
			(r"/v1/remove/foursquare", h.RemoveUserFoursquareHandler),
			(r"/v1/remove/flickr", h.RemoveUserFlickrHandler),
			(r"/v1/logout", h.LogoutHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			login_url="/login",
			twitter_consumer_key=models.AppSettings.objects[0].twitter_consumer_key,
			twitter_consumer_secret=models.AppSettings.objects[0].twitter_consumer_secret,
			facebook_api_key=models.AppSettings.objects[0].facebook_api_key,
			facebook_secret=models.AppSettings.objects[0].facebook_secret,
			fitbit_consumer_key=models.AppSettings.objects[0].fitbit_consumer_key,
			fitbit_consumer_secret=models.AppSettings.objects[0].fitbit_consumer_secret,
			zeo_consumer_key=models.AppSettings.objects[0].zeo_consumer_key,
			zeo_consumer_secret=models.AppSettings.objects[0].zeo_consumer_secret,
			foursquare_api_key=models.AppSettings.objects[0].foursquare_api_key,
			foursquare_client_id=models.AppSettings.objects[0].foursquare_client_id,
			foursquare_client_secret=models.AppSettings.objects[0].foursquare_client_secret,
			google_consumer_key=models.AppSettings.objects[0].google_consumer_key,
			google_consumer_secret=models.AppSettings.objects[0].google_consumer_secret,
			flickr_consumer_key=models.AppSettings.objects[0].flickr_consumer_key,
			flickr_consumer_secret=models.AppSettings.objects[0].flickr_consumer_secret,
			khanacademy_consumer_key=models.AppSettings.objects[0].khanacademy_consumer_key,
			khanacademy_consumer_secret=models.AppSettings.objects[0].khanacademy_consumer_secret,
			cookie_secret=models.AppSettings.objects[0].cookie_secret,
			debug=True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__": 
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application()) 
	http_server.listen(options.port) 
	tornado.ioloop.IOLoop.instance().start()

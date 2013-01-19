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
			(r"/", h.MainHandler),
			(r"/signup", h.SignUpHandler),
			(r"/login", h.LoginHandler),
			(r"/twitter", h.TwitterHandler),
			(r"/facebook", h.FacebookHandler),
			(r"/fitbit", h.FitbitHandler),
			(r"/zeo", h.ZeoHandler),
			(r"/foursquare", h.FoursquareHandler),
			(r"/google", h.GoogleHandler),
			(r"/flickr", h.FlickrHandler),
			(r"/khanacademy", h.KhanAcademyHandler),
			(r"/logout", h.LogoutHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
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

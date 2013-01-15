import tornado.web
import tornado.httpserver 
import tornado.ioloop 
import tornado.options
import os.path
from tornado.options import define, options

import handlers as h
# import models

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
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
			twitter_consumer_key='OaqpkBvltogUUjmeCqVhVw',
			twitter_consumer_secret= 'UPV2gSGAh6IfgYo123jJ4k4Sawjhd9JRp3l0QCOs',
			facebook_api_key='426446497428837',
			facebook_secret='7a811496573b875c107d3bafc1828cc2',
			fitbit_consumer_key='8f5e05187b294f0989eb8cb9b20de54c',
			fitbit_consumer_secret='0f88f60eae0142b586340594249e5f67',
			zeo_consumer_key='peter.darche',
			zeo_consumer_secret='Aiy0EeXeRae9AebilaiK1t',
			foursquare_api_key='MSJXJGSMPMWVEEZKGCF1YEHUIAZG5YW3U4U0CNRZJYJ5TPPC',
			foursquare_client_id='MSJXJGSMPMWVEEZKGCF1YEHUIAZG5YW3U4U0CNRZJYJ5TPPC',
			foursquare_client_secret='2CU20YV4WTEYKVQNKCXM51IMFDALG2RSLAHI5LGGMW0FSGBL',
			google_consumer_key='anonymous',
			google_consumer_secret='anonymous',
			flickr_consumer_key='89e19ea49458a66cf9aa8c980e898655',
			flickr_consumer_secret='03656cf0a41a75e1',
			khanacademy_consumer_key='ypzzb7hyX2Q9mVHR',
			khanacademy_consumer_secret='pfGvSc5adwCRCyE3',
			cookie_secret='NTliOTY5NzJkYTVlMTU0OTAwMTdlNjgzMTA5M2U3OGQ5NDIxZmU3Mg==',
			debug=True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__": 
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application()) 
	http_server.listen(options.port) 
	tornado.ioloop.IOLoop.instance().start()

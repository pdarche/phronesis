import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

################ SERVICE USER INFO MODELS ################
class FitbitAccessToken(EmbeddedDocument):
	key = StringField()
	encoded_user_id = StringField()
	secret = StringField()

class FitbitUserInfo(EmbeddedDocument):
	created_at = StringField()
	ftbt_user_name = StringField()
	ftbt_access_token = EmbeddedDocumentField(FitbitAccessToken)
	ftbt_weight_unit = StringField()
	ftbt_stride_length_walking = FloatField()
	ftbt_display_name = StringField()
	ftbt_foods_locale = StringField()
	ftbt_height_unit = StringField()
	ftbt_locale = StringField()
	ftbt_gender = StringField()
	ftbt_member_since = StringField()
	ftbt_offset_from_utc_millis = IntField()
	ftbt_encoded_id = StringField()
	ftbt_avatar = StringField()
	ftbt_water_unit = StringField()
	ftbt_distance_unit = StringField()
	ftbt_glucose_unit = StringField()
	ftbt_full_name = StringField()
	ftbt_nickname = StringField()
	ftbt_stride_length_running = FloatField()


class FoursquareUserInfo(EmbeddedDocument):
	created_at = StringField()
	foursquare_last_name = StringField()
	foursquare_first_name = StringField()
	foursquare_access_token = StringField()
	foursquare_user_photo = StringField()
	foursquare_pings = BooleanField()
	foursquare_home_city = StringField()
	foursquare_id = StringField()
	foursquare_bio = StringField()
	foursquare_relationship = StringField()
	foursquare_checkin_pings = StringField()


class FlickrAccessToken(EmbeddedDocument):
	username = StringField()
	secret = StringField()
	fullname = StringField()
	key = StringField()
	user_nsid = StringField()

class FlickrUserInfo(EmbeddedDocument):
	created_at = StringField() 			#add updates?
	flickr_access_token = EmbeddedDocumentField(FlickrAccessToken)
	flickr_stat = StringField()
	flickr_user_url = StringField()
	flickr_nsid = StringField()


class FacebookUserInfo(EmbeddedDocument):
	created_at = StringField()
	facebook_picture = StringField()
	facebook_first_name = StringField()
	facebook_last_name = StringField()
	facebook_name = StringField()
	facebook_locale = StringField()
	facebook_access_token = StringField()
	facebook_link = StringField()
	facebook_id = StringField()


class KhanAcademyAccessToken(EmbeddedDocument):
	khanacademy_secret = StringField()
	khanacademy_key = StringField()

class KhanAcademyUserInfo(EmbeddedDocument):
	created_at = StringField()
	khanacademy_has_notification = BooleanField()
	khanacademy_can_record_tutorial = BooleanField()
	khanacademy_is_demo = BooleanField()
	khanacademy_key_email = StringField()
	khanacademy_is_pre_phantom = BooleanField()
	khanacademy_developer = BooleanField()
	kahnacademy_user_id = StringField()
	khanacademy_is_google_user = BooleanField()
	khanacademy_profile_root = StringField()
	khanacademy_has_email_subscription = BooleanField()
	khanacademy_discussion_banned = BooleanField()
	khanacademy_is_phantom = BooleanField()
	khanacademy_email = StringField()
	khanacademy_is_facebook_user = BooleanField()
	khanacademy_is_midsignup_phantom = BooleanField()
	# khanacademy_auth_emails = ListField(StringField)
	khanacademy_last_modified_as_mapreduce_epoch = IntField()
	khanacademy_uservideocss_version = IntField()
	khanacademy_nickname = StringField()
	# khanacademy_user_input_auth_emails = ListField(StringField)
	khanacademy_kind = StringField()
	khanacademy_is_moderator_or_developer = BooleanField()
	khanacademy_joined = StringField()
	khanacademy_userprogresscache_version = IntField()
	khanacademy_gae_bingo_identity = StringField()


class TwitterUserInfo(EmbeddedDocument):
	created_at = StringField()
	twitter_default_profile_image = BooleanField()
	twitter_id = IntField()
	twitter_verified = BooleanField()
	twitter_profile_image_url_https = StringField()
	twitter_id_str = StringField()
	twitter_utc_offset = IntField()
	twitter_location = StringField()
	twitter_profile_image_url = StringField()
	twitter_geo_enabled = BooleanField()
	twitter_name = StringField()
	twitter_lang = StringField()
	twitter_screen_name = StringField()
	twitter_url = StringField()
	twitter_contributors_enabled = BooleanField() #remove?
	twitter_time_zone = StringField()
	twitter_protected = BooleanField()
	twitter_default_profile = BooleanField()	#remove?
	twitter_is_translator = BooleanField()		#remove?


class GoogleUserInfo(EmbeddedDocument):
	created_at = StringField()
	google_first_name = StringField()
	google_claimed_id = StringField()
	google_name = StringField()
	google_locale = StringField()
	google_last_name = StringField()
	google_email = StringField()


class OpenPathsUserInfo(EmbeddedDocument):
	created_at = StringField()
	op_access_key = StringField()
	op_access_secret = StringField()


class ZeoUserInfo(EmbeddedDocument):
	create_at = StringField()
	zeo_username = StringField()
	zeo_password = StringField()

class UserAdjectives(EmbeddedDocument):
	first_priority = StringField()
	first_priority_specific = StringField()
	second_priority = StringField()
	second_priority_specific = StringField()
	third_priority = StringField()
	third_priority_specific = StringField()
	

class User(Document):
	user_since = StringField()
	username = StringField()
	password = StringField()
	offset_from_utc_millis = IntField()
	time_zone = StringField()
	date_of_birth = DateTimeField()
	ftbt_user_info = EmbeddedDocumentField(FitbitUserInfo)
	foursquare_user_info = EmbeddedDocumentField(FoursquareUserInfo)
	flickr_user_info = EmbeddedDocumentField(FlickrUserInfo)
	facebook_user_info = EmbeddedDocumentField(FacebookUserInfo)
	khanacademy_user_info = EmbeddedDocumentField(KhanAcademyUserInfo)
	twitter_user_info = EmbeddedDocumentField(TwitterUserInfo)
	google_user_info = EmbeddedDocumentField(GoogleUserInfo)
	openpaths_user_info = EmbeddedDocumentField(OpenPathsUserInfo)
	zeo_user_info = EmbeddedDocumentField(ZeoUserInfo)
	adjectives = EmbeddedDocumentField(UserAdjectives)




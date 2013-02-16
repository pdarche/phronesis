import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

############# KHAN ACADEMY MODELS ############# 
class KhanAcademyVideo(EmbeddedDocument):
	date_added = DateTimeField()
	description = StringField()
	duration = IntField()
	ka_url = StringField()
	keywords = StringField()
	kind = StringField()
	playlists = ListField()
	readable_id = StringField()
	title = StringField()
	url = StringField()
	views = IntField()
	youtube_id = StringField()

class KhanAcademyVideoLog(EmbeddedDocument):
	kind = StringField()
	playlist_titles = ListField()
	points_earned = IntField()
	seconds_watched = IntField()
	time_watched = DateTimeField()
	user = StringField()
	video_title = StringField()

class KhanAcademyUserExercise(EmbeddedDocument):
	exercise = StringField()
	first_done = DateTimeField()
	kind = StringField()
	last_done = DateTimeField()
	last_review = DateTimeField()
	longest_streak = IntField()
	proficient_date = StringField()
	seconds_per_fast_problem = FloatField()
	streak = IntField()
	summative = BooleanField()
	total_done = IntField()
	user = StringField() 

class KhanAcademyUserVideos(EmbeddedDocument):
	completed = BooleanField()
	duration = IntField()
	kind = StringField()
	last_second_watched = IntField()
	last_watched = DateTimeField()
	points = IntField()
	seconds_watched = IntField()
	user = StringField()
	videos = ListField(EmbeddedDocumentField(KhanAcademyVideo))
	video_logs = ListField(EmbeddedDocumentField(KhanAcademyVideoLog))
	exercises = ListField(EmbeddedDocumentField(KhanAcademyUserExercise))

class KhanAcademyStats(Document):
	date = StringField()
	user_id = StringField()
	all_proficient_exercises = ListField()
	badge_counts = ListField()
	coaches = ListField()
	joined = DateTimeField()
	last_activity = DateTimeField()
	nickname = StringField()
	points = IntField()
	proficient_exercises = ListField()
	suggested_exercises = ListField()
	total_seconds_watched = IntField()
	khan_academy_user_id = StringField()
	prettified_user_email = StringField()



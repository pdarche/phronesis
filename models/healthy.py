import os, sys
from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

class Trait(Document):
	trait = StringField()


class TraitSpecific(Document):
	for_trait = StringField()
	trait_specific = StringField() 
	as_heading = StringField()
	info = StringField()


class RecommendedHabit(Document):
	for_trait = StringField()
	for_trait_specific = StringField()
	rec_habit = StringField()
	rec_habit_key = StringField()


class CurrentStatus(Document):
	for_trait = StringField()
	for_trait_specific = StringField()
	for_rec_habit = StringField()
	for_rec_habit_key = StringField()
	data_url = StringField()
	attr = StringField()


class ActionToTake(Document):
	for_trait = StringField()
	for_trait_specific = StringField()
	for_rec_habit = StringField()
	for_rec_habit_key = StringField()
	action = StringField()	


class Trigger(Document):
	username = StringField()
	for_action = StringField()
	for_rec_habit = StringField()
	for_trait_specific = StringField()
	for_trait = StringField()
	activation_time = IntField()
	location = GeoPointField()
	is_recurring = BooleanField()


# class CardiovascularHabits(Document):
# 	trait = StringField()
# 	habits_list = ListField()
# 	info = StringField()
# 	very_active_forty_five_minutes = EmbeddedDocumentField(u.HabitInfo)
# 	quit_smoking = EmbeddedDocumentField(u.HabitInfo)
# 	less_than_two_thousand_mg_sodium = EmbeddedDocumentField(u.HabitInfo)
# 	less_than_twenty_g_sat_fat = EmbeddedDocumentField(u.HabitInfo)
# 	one_drink_per_day = EmbeddedDocumentField(u.HabitInfo)


# class MusculoskeletalHabits(Document):
# 	trait = StringField()
# 	habits_list = ListField
# 	info = StringField()
# 	weight_training = EmbeddedDocumentField(u.HabitInfo)
# 	jogging = EmbeddedDocumentField(u.HabitInfo)
# 	stretch = EmbeddedDocumentField(u.HabitInfo)
# 	posture = EmbeddedDocumentField(u.HabitInfo)


# class RespiratoryHabits(Document):
# 	trait = StringField()
# 	habits_list = ListField()
# 	info = StringField()
# 	jogging = EmbeddedDocumentField(u.HabitInfo)
# 	quit_smoking = EmbeddedDocumentField(u.HabitInfo)


# class MentalHealthHabits(Document):
# 	trait = StringField()
# 	habits_list = ListField()
# 	info = StringField()
# 	sufficient_sleep = EmbeddedDocumentField(u.HabitInfo)
# 	reduce_stress = EmbeddedDocumentField(u.HabitInfo)
# 	have_sex = EmbeddedDocumentField(u.HabitInfo)

# class Healthy(Document):
# 	specifics_list = ListField()
# 	cardiovascular = EmbeddedDocumentField(CardiovascularHabits)
# 	musculoskeletal = EmbeddedDocumentField(MusculoskeletalHabits)
# 	respiratory = EmbeddedDocumentField(RespiratoryHabits)
# 	mental = EmbeddedDocumentField(MentalHealthHabits)




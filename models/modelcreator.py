import os
import sys
import types
from itertools import groupby
import time

from mongoengine import *
import mongoengine
import simplejson
from bson.objectid import ObjectId

import healthy
import useractions as u

connect('local_db')

traits = [
	"healthy", "sustainable", "intelligent",
	"generous", "productive", "focused",
	"attentive", "kind", "punctual", "just",
	"disciplined", "honest", "respectful",
	"responsible", "educated", "wise"
]

for trait in traits:
	newTrait = healthy.Trait(
			trait = trait	
	)

	# if newTrait.save():
	# 	print "saved new trait"
	# else:
	# 	print "didn't save"


trait_specifics = [

	{ "trait_specific_name" : "cardiovascular", "for_trait" : "healthy", "as_heading" : "improve my cardiovascular health", "info" : ""},
	{ "trait_specific_name" : "musculoskelatal", "for_trait" : "healthy", "as_heading" : "improve my musculoskelatal health", "info" : "" },
	{ "trait_specific_name" : "mental_health", "for_trait" : "healthy", "as_heading" : "improve my mental health", "info" : ""},
	{ "trait_specific_name" : "respiratory", "for_trait" : "healthy", "as_heading" : "improve my respiratory health", "info" : ""},
	
	{ "trait_specific_name" : "carbon", "for_trait" : "sustainable", "as_heading" : "reduce carbon footprint", "info" : ""},
	{ "trait_specific_name" : "waste", "for_trait" : "sustainable", "as_heading" : "reduce waste" , "info" : ""},
	{ "trait_specific_name" : "energy", "for_trait" : "sustainable", "as_heading" : "reduce energy use", "info" : ""},
	{ "trait_specific_name" : "meat_consumption", "for_trait" : "sustainable", "as_heading" : "reduce meat consumption", "info" : ""},
	
	{ "trait_specific_name" : "scientific","for_trait" : "educated", "as_heading" : "expand my scientific knowledge", "info" : ""},
	{ "trait_specific_name" : "literary","for_trait" : "educated", "as_heading" : "expand my literary knowledge", "info" : ""},
	{ "trait_specific_name" : "historical","for_trait" : "educated", "as_heading" : "expand my historical knowledge", "info" : ""},
	{ "trait_specific_name" : "social_scientific", "for_trait" : "educated", "as_heading" : "expand my social scientific knowledge", "info" : "" },
	{ "trait_specific_name" : "mathematical", "for_trait" : "educated", "as_heading" : "expand my social mathematical knowledge", "info" : "" }

]

for ts in trait_specifics:
	newTs = healthy.TraitSpecific(
		for_trait = ts["for_trait"],
		trait_specific = ts["trait_specific_name"],
		as_heading = ts["as_heading"],
		info = ts["info"]
	)

	# if newTs.save():
	# 	print "saved new trait spec"
	# else:
	# 	print "didn't save"


reco_habits = [
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "rh" : "be very active for 45 minutes per day", "rhk" : "vaff" },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "rh" : "quit smoking", "rhk" : "qs" },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "rh" : "limit saturated fat intake to 20g per day", "rhk" : "sfg" },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "rh" : "limit sodium intatke to 2400mg per day", "rhk" : "smg" },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "rh" : "limit alchohol consumption to 1 drink per day (avg)", "rhk" : "lac" },

	{ "for_trait" : "healthy", "for_trait_specific" : "musculoskelatal", "rh" : "weight train 2 days per week", "rhk" : "wt" },
	{ "for_trait" : "healthy", "for_trait_specific" : "musculoskelatal", "rh" : "stretch for 20 minutes before working out", "rhk" : "stretch" },
	{ "for_trait" : "healthy", "for_trait_specific" : "musculoskelatal", "rh" : "work at a standing dest", "rhk" : "standingdesk" },
	{ "for_trait" : "healthy", "for_trait_specific" : "musculoskelatal", "rh" : "maintain good posture", "rhk" : "posture" },
	
	{ "for_trait" : "healthy", "for_trait_specific" : "respiratory", "rh" : "quit smoking", "rhk" : "qs" },
	{ "for_trait" : "healthy", "for_trait_specific" : "respiratory", "rh" : "be very active for 45 minutes per day", "rhk" : "vaff" },

	{ "for_trait" : "healthy", "for_trait_specific" : "mental_health", "rh" : "get more than 7 hours of sleep", "rhk" : "shs" },
	{ "for_trait" : "healthy", "for_trait_specific" : "mental_health", "rh" : "keep stress levels below 20 stress-os", "rhk" : "stress" }
]


for rh in reco_habits:
	newRh = healthy.RecommendedHabit(
		for_trait = rh["for_trait"],
		for_trait_specific = rh["for_trait_specific"],
		rec_habit = rh["rh"],
		rec_habit_key = rh["rhk"]
	)

	# if newRh.save():
	# 	print "new hr saved"
	# else:
	# 	print "new rh didn't save"


actions = [
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "be very active for 45 minutes per day", "action" : "take the stairs", "rhk" : "vaff" },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "be very active for 45 minutes per day", "action" : "walk an extra subway stop", "rhk" : "vaff" },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "be very active for 45 minutes per day", "action" : "try jogging", "rhk" : "vaff" },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "be very active for 45 minutes per day", "action" : "play an organized sport", "rhk" : "vaff" },

	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "quit smoking", "action" : "use the patch", "rhk" : "qs"},
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "quit smoking", "action" : "use e-cigarettes", "rhk" : "qs"},
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "quit smoking", "action" : "get lost on an island for a month", "rhk" : "qs"},

	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "limit saturated fat intake to 20g per day", "action" : "eat fewer animal products", "rhk" : "sfg" },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "limit saturated fat intake to 20g per day", "action" : "eat less pizza", "rhk" : "sfg"  },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "limit saturated fat intake to 20g per day", "action" : "eat fewer burritos", "rhk" : "sfg"  },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "limit saturated fat intake to 20g per day", "action" : "leave off one ingredient", "rhk" : "sfg"  },

	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "limit sodium intake to 2400mg per day", "action" : "eat fewer packaged foods", "rhk" : "smg" },
	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "limit sodium intake to 2400mg per day", "action" : "leave off a salty ingredient", "rhk" : "smg" },

	{ "for_trait" : "healthy", "for_trait_specific" : "cardiovascular", "for_rh" : "limit alchohol consumption to one drink", "action" : "nurse your beer", "rhk" : "lac" }
]

for aa in actions:
	newAtT = healthy.ActionToTake(
		for_trait = aa["for_trait"],
		for_trait_specific = aa["for_trait_specific"],
		for_rec_habit = aa["for_rh"],
		for_rec_habit_key = aa["rhk"],
		action = aa["action"]
	)

	# if newAtT.save():
	# 	print "att saved"
	# else: 
	# 	print "att not saved"


csus = [
	{ "for_trait" : "healthy" , "for_trait_specific" : "cardiovascular", "for_rh" : "be very active for 45 minutes per day", "url" : "/v1/data/pdarche/body/physicalActivity", "attr" : "mins_highly_active", "rhk" : "vaff" },
	{ "for_trait" : "healthy" , "for_trait_specific" : "cardiovascular", "for_rh" : "limit saturated fat intake to 20g per day", "url" : "/v1/data/pdarche/body/nutrition", "attr" : "saturated_fat", "rhk" : "sfg" },
	{ "for_trait" : "healthy" , "for_trait_specific" : "cardiovascular", "for_rh" : "limit sodium intake to 2400mg per day", "url" : "/v1/data/pdarche/body/nutrition", "attr" : "sodium", "rhk" : "smg" },
	{ "for_trait" : "healthy" , "for_trait_specific" : "cardiovascular", "for_rh" : "limit alchohol consumption to one drink", "url" : "/v1/data/pdarche/body/nutrition", "attr" : "drink", "rhk" : "lac" },
]

for cs in csus:
	newCS = healthy.CurrentStatus(
		for_trait = cs["for_trait"],
		for_trait_specific = cs["for_trait_specific"],
		for_rec_habit = cs["for_rh"],
		for_rec_habit_key = cs["rhk"],
		data_url = cs["url"],
		attr = cs["attr"]
	)

	# if newCS.save():
	# 	print "cs saved"
	# else:
	# 	print "cs didn't save"

# vaffm = u.HabitInfo(
# 		url = '/veryActiveFortyFive',
# 		actions = ["take the stairs", "walk an extra subway stop", "go jogging", "participate in organized sports" ],
# 		triggers = []
# 	)

# qs = u.HabitInfo(
# 		url = '/stopSmoking',
# 		actions = ["nicotein gum", "the patch", "herbs" ],
# 		triggers = []
# 	)

# sodium = u.HabitInfo(
# 		url = '/sodium',
# 		actions = ["eat less packaged food", "leave off an ingredient" ],
# 		triggers = []
# 	)

# sat_fat = u.HabitInfo(
# 		url = '/saturatedFat',
# 		actions = [ "leave off an ingredient", "eat fewer animal products" ],
# 		triggers = []
# 	)

# drink = u.HabitInfo(
# 		url = '/oneDrink',
# 		actions = [ "nurse you beer", "track consumption" ],
# 		triggers = []
# 	)

# cardio_habits = [
# 	"Be Very Active for 45 Minutes", "Quit Smoking",
# 	"Consume Less Than 2400mg of Sodium",
# 	"Consume Less Than 20g of Saturated Fat",
# 	"Average Less Than One Alcholic Beverage Per Day"
# ]

# cardio = healthy.CardiovascularHabits(
# 		habits_list = cardio_habits,
# 		info = "test info there will be some other string here",
# 		very_active_forty_five_mintutes = vaffm,
# 		quit_smoking = qs,
# 		less_than_two_thousand_mg_sodium = sodium,
# 		less_than_twenty_g_sat_fat = sat_fat,
# 		one_drink_per_day = drink
# 	)



# # MS HABITS 

# jog = u.HabitInfo(
# 		url = '/jog',
# 		actions = [ "run around mccaren park", "run around the city"],
# 		triggers = []
# 	)

# wt = u.HabitInfo(
# 		url = '/weightTraining',
# 		actions = ["nicotein gum", "the patch", "herbs" ],
# 		triggers = []
# 	)

# stretch = u.HabitInfo(
# 		url = '/stretch',
# 		actions = ["stretch for 20 minuts before any exercise"],
# 		triggers = []
# 	)

# posture = u.HabitInfo(
# 		url = '/posture',
# 		actions = [ "use a standing desk", "don't slouch" ],
# 		triggers = []
# 	)

# ms_habits = [
# 	"Jog 30 Minutes Per Day", 
# 	"Stretch 20 Minutes Per Day",
# 	"Low Impact Weight Training",
# 	"Work on you posture"
# ]

# ms = healthy.MusculoskeletalHabits(
# 		habits_list = cardio_habits,
# 		info = "test info there will be some other string here",
# 		weight_training = wt,
# 		jogging = jog,
# 		stretch = stretch,
# 		posture = posture
# 	)

# # RES HABITS

# res_habits = [
# 	"Jog 30 Minutes Per Day"
# 	"Quit Smoking"
# ]

# respiratory = healthy.RespiratoryHabits(
# 		habits_list = res_habits,
# 		info = "test info there will be some other string here",
# 		jogging = jog,
# 		quit_smoking = qs
# 	)

# # MENTAL HEALTH

# sleep = u.HabitInfo(
# 		url = '/sufficientSleep',
# 		actions = [ "maintain a consitent bed time", "use a blackout curtain", "don't drink caffiene after 6:00 pm" ],
# 		triggers = []
# 	)

# stress = u.HabitInfo(
# 		url = '/reduceStress',
# 		actions = [ "get your shit done" ],
# 		triggers = []
# 	)

# sex = u.HabitInfo(
# 		url = '/haveSex',
# 		actions = [ "make more money" ],
# 		triggers = []
# 	)

# mh_habits = [
# 	"Get Sufficient Sleep", "Reduced Stress Levels",
# 	"Have Sex"
# ]

# mental = healthy.MentalHealthHabits(
# 		habits_list = mh_habits,
# 		info = "test info there will be some other string here",
# 		sufficient_sleep = sleep,
# 		reduce_stress = stress,
# 		have_sex = sex
# 	)


# specifics_list = [
# 	"Cardiovascular Health", "Musculoskeletal Health",
# 	"Respiratory Health", "Mental Health"
# ]

# # healthy = healthy.Healthy(
# # 		specifics_list = specifics_list,
# # 		cardiovascular = cardio,
# # 		musculoskeletal = ms,
# # 		respiratory = respiratory,
# # 		mental = mental
# # 	)

# if cardio.save():
# 	print "cardio saved"
# else:
# 	print "not saved"

# if ms.save():
# 	print "ms saved"
# else:
# 	print "not saved"

# if respiratory.save():
# 	print "res saved"
# else:
# 	print "not saved"

# if mental.save():
# 	print "saved"
# else:
# 	print "not saved"


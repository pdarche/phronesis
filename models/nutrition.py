import os, sys

from mongoengine import *
from mongoengine_extras.fields import AutoSlugField
from mongoengine_extras.fields import SlugField

from datetime import datetime

class StandardLabelNutritionInfo(EmbeddedDocument):
	calories = FloatField()
	calories_from_fat = FloatField()
	total_fat = FloatField()
	saturated_fat = FloatField()
	trans_fat = FloatField()
	cholesterol = FloatField()
	sodium = FloatField()
	total_carbs = FloatField()
	dietary_fiber = FloatField()
	sugar = FloatField()
	protein = FloatField()
	vit_a = IntField()
	vit_c = IntField()
	calcium = IntField()
	iron = IntField()


class MyPyramidNutritionInfo(EmbeddedDocument):
	food_code = IntField()
	display_name = StringField()
	portion_default = FloatField()
	portion_amount = FloatField()
	portion_display_name = StringField()
	factor = FloatField()
	increment = FloatField()
	multiplier = FloatField()
	grains = FloatField()
	whole_grains = FloatField()
	vegetables = FloatField()
	orange_vegetables = FloatField()
	drkgreen_vegetables = FloatField()
	starchy_vegetables = FloatField()
	other_vegetables = FloatField()
	fruits = FloatField()
	milk = FloatField()
	meats = FloatField()
	soy = FloatField()
	drybeans_peas = FloatField()
	oils = FloatField()
	solid_fats = FloatField()
	added_sugars = FloatField()
	alcohol = FloatField()
	calories = FloatField()
	saturated_fats = FloatField()


class NutritionRecord(Document):
	phro_create_at = IntField()
	username = StringField()
	create_at = IntField()
	img_url = UrlField()
	name = StringField()
	pyramid_name = StringField()
	venue = StringField()
	venue_category String()
	loc = GeopointField()
	my_pyramid = EmbeddedDocumentField(MyPyramidNutritionInfo())
	standard_label = EmbeddedDocumentField(StandardLabelNutritionInfo())
	# sr_25 = EmbeddedDocumentField(SR25NutritionInfo())


# class SR25NutritionInfo(EmbeddedDocument):

class SR25FoodDescription(Document):
	NBD_No = StringField()
	FdGrp_Cd = StringField()
	Long_Desc = StringField()
	Shrt_Desc = StringField()
	ComName = StringField()
	ManufacName = StringField()
	Survey = StringField()
	Ref_desc = StringField()
	Refuse = FloatField()
	SciName = StringField()
	N_Factor = FloatField()
	Pro_Factor = FloatField()
	Fat_Factor = FloatField()
	CHO_Factor = FloatField()


class SR25LanguaLFactor(Document):
	NDB_No = IntField()
	Factor_Code = IntField()


class SR25LangauLFactorsDescription(Document):
	Factor_Code = IntField()
	Descrtiption = IntField()


class SR25NutrientData(Document):
	NDB_No = IntField()
	Nutr_No = IntField()
	Nutr_Val = FloatField()
	Num_Data_Pts = FloatField()
	Std_Error = FloatField()
	Src_Cd = StringField()
	Deriv_Cd = StringField()
	Ref_NDB_No = StringField()
	Add_Nutr_Mark = StringField()
	Num_Studies = IntField()
	Min = FloatField()
	Max = FloatField()
	DF = IntField()
	Low_EB = FloatField()
	Up_EB = FloatField()
	Stat_cmt = IntField()
	AddMod_Date = IntField()
	CC = IntField()


class SR25NutrientDefinition(Document):
	Nutr_No = StringField()
	Units = StringField()
	Tagname = StringField()
	NutrDesc = StringField()
	Num_Dec = StringField()
	SR_Order = IntField()


class SR25SourceCode(Document):
	Scr_Cd = StringField()
	SrcCd_Desc = StringField()


class SR25DataDerivation(Document):
	Deriv_Cd = StringField()
	Deriv_Desc = StringField()


class SR25Weight(Document):
	NDB_No = StringField()
	Seq = StringField()
	Amount = FloatField()
	Msre_Desc = StringField()
	Gm_Wgt = FloatField()
	Num_Data_Pts = IntField()
	Std_Dev = FloatField()













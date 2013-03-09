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
	img_url = URLField()
	name = StringField()
	pyramid_name = StringField()
	venue = StringField()
	venue_category = StringField()
	loc = GeoPointField()
	# my_pyramid = EmbeddedDocumentField(MyPyramidNutritionInfo())
	# standard_label = EmbeddedDocumentField(StandardLabelNutritionInfo())
	# sr_25 = EmbeddedDocumentField(SR25NutritionInfo())


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
	NDB_No = StringField()
	Nutr_No = StringField()
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
	Stat_cmt = StringField()
	AddMod_Date = StringField()
	CC = StringField()


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


class SR25FoodGroup(Document):
	FdGrp_Cd = StringField()
	FdGrp_Desc = StringField()


class SR25Weight(Document):
	NDB_No = StringField()
	Seq = StringField()
	Amount = FloatField()
	Msre_Desc = StringField()
	Gm_Wgt = FloatField()
	Num_Data_Pts = IntField()
	Std_Dev = FloatField()


class SR25Footnote(Document):
	NDB_No = StringField()
	Footnt_No = StringField()
	Footnt_Typ = StringField()
	Nutr_No = StringField()
	Footnt_Tx = StringField()


class SR25SourceLink(Document):
	NDB_No = StringField()
	Nutr_No = StringField()
	DataSrc_ID = StringField


class SR25SourceData(Document):
	DataSrc_ID = StringField()
	Authors = StringField()
	Title = StringField()
	Year = StringField()
	Journal = StringField()
	Vol_City = StringField()
	Issue_State = StringField()
	Start_Page = StringField()
	End_Page = StringField()


class SR25Abbrev(Document):
	NDB_No = StringField()
	Shrt_Desc = StringField()
	Water = FloatField()
	Energ_Kcal = IntField()
	Protein = FloatField()
	Lipid_Tot = FloatField()
	Ash = FloatField()
	Carbohydrt = FloatField()
	Fiber_TD = FloatField()
	Sugar_Tot = FloatField()
	Calcium = IntField()
	Iron = FloatField()
	Magnesium = IntField()
	Potassium = IntField()
	Sodium = IntField()
	Zinc = FloatField()
	Copper = FloatField()
	Manganese = FloatField()
	Selenium = FloatField()
	Vit_C = FloatField()
	Thiamin = FloatField()
	Riboflavin = FloatField()
	Niacin = FloatField()
	Panto_acid = FloatField()
	Vit_B6 = FloatField()
	Folate_Tot = FloatField()
	Folic_acid = IntField()
	Food_Folate = IntField()
	Folate_DFE = IntField()
	Choline_Tot = IntField()
	Vit_B12 = FloatField()
	Vit_A_IU = FloatField()
	Vit_A_RAE = IntField()
	Retinol = IntField()
	Alpha_Carot = IntField()
	Beta_Carot = IntField()
	Beta_Crypt = IntField()
	Lycopene = IntField()
	LutZea = IntField()
	Vit_E = FloatField()
	Vit_D_mcg = FloatField()
	Vit_D_IU = FloatField()
	Vit_K = FloatField()
	FA_Sat = FloatField()
	FA_Mono = FloatField()
	FA_Poly = FloatField()
	Cholestrl = FloatField()
	GmWt_1 = FloatField()
	GmWt_Desc1 = StringField()
	GmWt_2 = FloatField()
	GmWt_Desc2 = StringField()
	Refuse_Pct = FloatField()








# from types import ModuleType
import os
import sys
import types
from itertools import groupby
from mongoengine import *
import mongoengine
import simplejson
from bson.objectid import ObjectId

from xml.dom.minidom import parse, parseString
import models.mypyramid as pyramid

def encode_model(obj):
    if isinstance(obj, (mongoengine.Document, mongoengine.EmbeddedDocument)):
        out = dict(obj._data)
        for k,v in out.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
    elif isinstance(obj, mongoengine.queryset.QuerySet):
        out = list(obj)
    elif isinstance(obj, types.ModuleType):
        out = None
    elif isinstance(obj, groupby):
        out = [ (g,list(l)) for g,l in obj ]
    elif isinstance(obj, (list,dict)):
        out = obj
    else:
        raise TypeError, "Could not JSON-encode type '%s': %s" % (type(obj), str(obj))
    return out
    """
    and use this line " result = simplejson.dumps(base, default=encode_model)   "
    Example
    """

def parse_pyramid():
    connect('local_db')

    doc = parse('data/MyfoodapediaData/Food_Display_Table.xml')
    foods = doc.getElementsByTagName('Food_Display_Row')

    for food in foods:
        new_food = pyramid.MyPyramidReferenceInfo(
                food_code = food.getElementsByTagName('Food_Code')[0].firstChild.nodeValue,
                display_name = food.getElementsByTagName('Display_Name')[0].firstChild.nodeValue,
                portion_default = float(food.getElementsByTagName('Portion_Default')[0].firstChild.nodeValue),
                portion_amount = float(food.getElementsByTagName('Portion_Amount')[0].firstChild.nodeValue),
                portion_display_name = food.getElementsByTagName('Portion_Display_Name')[0].firstChild.nodeValue,
                factor = float(food.getElementsByTagName('Factor')[0].firstChild.nodeValue) if len(food.getElementsByTagName('Factor')) > 0 else None,
                increment = float(food.getElementsByTagName('Increment')[0].firstChild.nodeValue),
                multiplier = float(food.getElementsByTagName('Multiplier')[0].firstChild.nodeValue),
                grains = float(food.getElementsByTagName('Grains')[0].firstChild.nodeValue),
                whole_grains = float(food.getElementsByTagName('Whole_Grains')[0].firstChild.nodeValue),
                vegetables = float(food.getElementsByTagName('Vegetables')[0].firstChild.nodeValue),
                orange_vegetables = float(food.getElementsByTagName('Orange_Vegetables')[0].firstChild.nodeValue),
                drkgreen_vegetables = float(food.getElementsByTagName('Drkgreen_Vegetables')[0].firstChild.nodeValue),
                starchy_vegetabels = float(food.getElementsByTagName('Starchy_vegetables')[0].firstChild.nodeValue),
                other_vegetables = float(food.getElementsByTagName('Other_Vegetables')[0].firstChild.nodeValue),
                fruits = float(food.getElementsByTagName('Fruits')[0].firstChild.nodeValue),
                milk = float(food.getElementsByTagName('Milk')[0].firstChild.nodeValue),
                meats = float(food.getElementsByTagName('Meats')[0].firstChild.nodeValue),
                soy = float(food.getElementsByTagName('Soy')[0].firstChild.nodeValue),
                drybeans_peas = float(food.getElementsByTagName('Drybeans_Peas')[0].firstChild.nodeValue),
                oils = float(food.getElementsByTagName('Oils')[0].firstChild.nodeValue),
                solid_fats = float(food.getElementsByTagName('Solid_Fats')[0].firstChild.nodeValue),
                added_sugars = float(food.getElementsByTagName('Added_Sugars')[0].firstChild.nodeValue),
                alcohol = float(food.getElementsByTagName('Alcohol')[0].firstChild.nodeValue),
                calories = float(food.getElementsByTagName('Calories')[0].firstChild.nodeValue),
                saturated_fats = float(food.getElementsByTagName('Saturated_Fats')[0].firstChild.nodeValue)
            )
        
        if new_food.save():
            print "food saved"
        else:
            print "didn't save"


def remove_records():
    connect('local_db')

    foods = pyramid.MyPyramidReferenceInfo.objects()
    foods.delete()

    print len(foods)




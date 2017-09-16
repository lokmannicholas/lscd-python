#import sys
import json
from pymongo import MongoClient

host = ""
port = 27017
database = ""
with open('config.json') as json_data:
	config = json.load(json_data)
	host = config["mongo"]["host"]
	port = config["mongo"]["port"]
	database = config["mongo"]["database"]

cursor = 0

def dbConnect():
	global db
	global cursor
	client = MongoClient(host,port)
	db = client[database]
	cursor = 1

def getAllData(table):
	result = []
	if cursor == 0:
		dbConnect()
	all_data = getattr(db, table).find()
	for _data in all_data:
		result.append(_data)
	return result
	
def getFirstData(table):
	if cursor == 0:
		dbConnect()
	return getattr(db, table).find_one()	

def getSize(table):
	if cursor == 0:
		dbConnect()
	return getattr(db, table).count()

def save(table,post,updateKey):
	if cursor == 0:
		dbConnect()
	return getattr(db, table).update(updateKey, {"$set": post},upsert = True)
	
def saveAll(table,post):
	if cursor == 0:
		dbConnect()
	return getattr(db, table).insert_many(post).inserted_ids

def getAllData(table,searchable_data):
	result = []
	if cursor == 0:
		dbConnect()
	all_data = getattr(db, table).find(searchable_data)
	for _data in all_data:
		result.append(_data)
	return result

def getAllData(table,searchable_data,sort_value):
	result = []
	if cursor == 0:
		dbConnect()
	all_data = getattr(db, table).find(searchable_data).sort(sort_value)
	for _data in all_data:
		result.append(_data)
	return result

def getFirstData(table,searchable_data):
	if cursor == 0:
		dbConnect()
	return getattr(db, table).find_one(searchable_data)	

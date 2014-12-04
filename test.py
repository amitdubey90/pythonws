from bottle import route, run, request
from pymongo import MongoClient
import json
import MySQLdb

client = MongoClient('ec2-54-67-57-228.us-west-1.compute.amazonaws.com', 27017)
mongoDB = client.pydb
shirtCol = mongoDB.shirts


db = MySQLdb.connect(host="localhost", # your host, usually localhost
					user="root", # your username
					passwd="summer", # your password
					db="pydb") # name of the data base
cursor = db.cursor()

@route('/shirt/<shirtID>', method='GET')
def getShirt( shirtID=1234 ):
	doc = shirtCol.find_one({"shirtId":shirtID},{"_id":0})
	return doc

@route('/shirts', method="PUT")
def updateShirt():
	doc = request.json
	print "doc is %s" % doc
	shirtCol.update({"shirtId": doc['shirtId']}, doc)
	return { "success" : True}

@route('/shirts', method='DELETE' )
def deleteShirts():
	doc = request.json
	shirtCol.remove({"shirtId" : doc['shirtId']})
	return { "success" : True}

@route('/shirts', method='POST')
def insertShirt():
	
	#print "inside post"
	doc = request.json
	id = shirtCol.insert(doc)
	
	return { "success" : True }

@route('/shoe/<shoeId>', method='GET')
def getShirt(shoeId="1"):
	
	cursor.execute("SELECT shoeId, shoeName, shoeQuantity, createdBy FROM SHOE_TABLE where shoeId = %s" % shoeId)
	
	row = cursor.fetchone()
	
	return {"shoeId": row[0], "shoeName": row[1], "shoeQuantity": row[2], "createdBy": row[3]}

@route('/shoes', method="PUT")
def updateShirt():
	doc = request.json
	
	return { "success" : True}

@route('/shoes', method='DELETE' )
def deleteShirts():
	doc = request.json
	cursor.execute("DELETE From SHOE_TABLE where shoeId= %s" %doc['shoeId'])
	return { "success" : True}

@route('/shoes', method='POST')
def insertShirt():
	
	doc = request.json
	query = "Insert into SHOE_TABLE (shoeId, shoeName, shoeQuantity, createdBy) values (%s, %s, %s, %s)"
	cursor.execute(query, (doc['shoeId'], doc['shoeName'], doc['shoeQuantity'], doc['createdBy']))	
	return { "success" : True }

run(host='localhost', port=8080, debug=True)
	
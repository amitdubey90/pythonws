from bottle import route, run, request
from pymongo import MongoClient
import json
import MySQLdb
import datetime
from bson import json_util

client = MongoClient('localhost', 27017)
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
	doc['createdDate'] = doc['createdDate'].strftime("%Y-%m-%d")
	return doc
	#return json.dumps(doc, default=json_util.default)

@route('/shirts', method="PUT")
def updateShirt():
	doc = request.json
	print "doc is %s" % doc
	olddoc = shirtCol.find_one({"shirtId":doc['shirtId']},{"_id":0})
	doc['createdDate'] = olddoc['createdDate']
	shirtCol.update({"shirtId": doc['shirtId']}, doc)
	return { "success" : True}

@route('/shirts', method='DELETE' )
def deleteShirts():
	doc = request.json
	shirtCol.remove({"shirtId" : doc['shirtId']})
	return { "success" : "OK"}

@route('/shirts', method='POST')
def insertShirt():
	
	#print "inside post"
	doc = request.json
	doc['createdDate'] = datetime.datetime.now();
	print "doc is %s" % doc
	id = shirtCol.insert(doc)
	return { "success" : "OK" }

@route('/shoe/<shoeId>', method='GET')
def getShirt(shoeId="1"):
	
	cursor.execute("SELECT shoeId, shoeName, shoeQuantity, createdBy, createdDate FROM SHOE_TABLE where shoeId = %s" % shoeId)
	
	row = cursor.fetchone()
	
	return {"shoeId": row[0], "shoeName": row[1], "shoeQuantity": row[2], "createdBy": row[3], "createdDate": row[4]}

@route('/shoes', method="PUT")
def updateShirt():
	doc = request.json
	
	return { "success" : "OK"}

@route('/shoes', method='DELETE' )
def deleteShirts():
	doc = request.json
	cursor.execute("DELETE From SHOE_TABLE where shoeId= %s" %doc['shoeId'])
	return { "success" : "OK"}

@route('/shoes', method='POST')
def insertShirt():
	
	doc = request.json
	query = "Insert into SHOE_TABLE (shoeId, shoeName, shoeQuantity, createdBy, createdDate) values (%s, %s, %s, %s, %s)"
	cursor.execute(query, (doc['shoeId'], doc['shoeName'], doc['shoeQuantity'], doc['createdBy'], datetime.datetime.now().strftime("%Y-%m-%d")))	
	db.commit()
	return { "success" : "OK" }

if __name__ == "__main__":
	run(host='localhost', port=8080)
	
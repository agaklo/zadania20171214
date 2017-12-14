from pymongo import MongoClient
from pprint import pprint
import random
import argparse
import json

#CONNECTION_STRING="mongodb://localhost:27017"
CONNECTION_STRING="mongodb://visitor:visitorpass@ds129706.mlab.com:29706/gisslab"
DATABASE_NAME ="gisslab" 
COLLECTION_NAME ="gisscol17" 
DEFAULT_RESULT_FILE = "result.json"

def insert_data(collection):	
    for i in range(500):
	collection.insert_one({"id": i,"val": random.randint(0,19)})

def get_data(collection):
    histogram = {}
    cursor = collection.find()
    
    for document in cursor:
        val = document['val']
        if val not in histogram.keys():
            histogram[val] = 0
        histogram[val] = histogram[val]+1
    return histogram

def write_output(file_name, data):
    with open(file_name, 'w') as f:
        f.write(json.dumps(data))


if __name__== '__main__':
    parser = argparse.ArgumentParser("test")
    parser.add_argument("command", 
	help="Issue command to insert data to database or select statistics", 
	choices=['insert','select'],); 
    args = parser.parse_args()

    client = MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    if args.command == "insert":
        print ("Script will put 500 new records to database %s "\
                "and collection %s" % (DATABASE_NAME, COLLECTION_NAME) )
        insert_data(collection)
    elif args.command == "select":
        print ("Script will select statistics and write it to: " + DEFAULT_RESULT_FILE)
        write_output(DEFAULT_RESULT_FILE, get_data(collection) )
    else:
        print ("Unknown command: " +args.command)

from flask import Flask
import pandas as pd
import os
from pymongo import MongoClient

HOST = str(os.environ["MONGO_HOST"])
PORT = int(os.environ["MONGO_PORT"])
USERNAME = str(os.environ["MONGO_USER"])
PASSWORD = str(os.environ["MONGO_PASSWORD"])
DB = str(os.environ["MONGO_DATABASE"])
COLLECTION = str(os.environ["MONGO_COLLECTION"])

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)


    return conn[db]

def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    global HOST, PORT, USERNAME, PASSWORD, DB
    df = read_mongo(host=HOST, port=PORT, username=USERNAME, password=PASSWORD, db=DB, collection=)
    return df.to_html()

app.run(host="0.0.0.0")
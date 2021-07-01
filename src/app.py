from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
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
    if "createdAt" in list(df.columns):
        df = df.set_index("createdAt")
        df = df.sort_values(by="createdAt", ascending=False)

    return df

app = Flask(__name__)
auth = HTTPBasicAuth()

if "VIEWERUSER" in os.environ and "VIEWERPWHASH" in os.environ:
    USER = os.environ["VIEWERUSER"]
    PWHASH = os.environ["VIEWERPWHASH"]
else:
    # user test, pw test
    USER = "test"
    PWHASH = "pbkdf2:sha256:260000$fAVIMeJbnuBR66K0$5506472ab0bcf53f43b39c27a62fed0c3c6fa59063ed20c90873c1d41c53ca1e"

users = {
    USER:PWHASH
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route("/", methods = ['GET'])
@auth.login_required
def index():
    global HOST, PORT, USERNAME, PASSWORD, DB
    df = read_mongo(host=HOST, port=PORT, username=USERNAME, password=PASSWORD, db=DB, collection=COLLECTION)
    return df.to_html()

app.run(host="0.0.0.0")
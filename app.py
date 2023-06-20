import os
import datetime
from flask import Flask, Response, request, jsonify
from dotenv import load_dotenv
from flask_cors import cross_origin
from pymongo import MongoClient
from bson.json_util import dumps


load_dotenv()

app = Flask(__name__)
mongo_db_url = os.environ.get("DB_CONN_STRING")

client = MongoClient(mongo_db_url)
db = client['Website']

@app.post("/api/comments")
@cross_origin()
def add_comment():
    _json = request.json
    now = datetime.datetime.now()
    _json["datetime"] = now.strftime('%Y-%m-%d %H:%M:%S')
    print(_json)
    db.Comments.insert_one(_json)

    res = jsonify({"message": "Comment added successfully"})
    res.status_code = 200
    return res

@app.get("/api/comments")
def get_comments():
    print(mongo_db_url)
    comments = list(db.Comments.find())
    print("after db")
    res = Response(
        response = dumps(comments), status=200,  mimetype="application/json")
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res
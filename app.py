from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from marshmallow import Schema, fields
from bson.json_util import dumps
from json import loads

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://week3:1yDxm2EdXKkIwby4@cluster0.xtk0f.mongodb.net/fruit_basket?retryWrites=true&w=majority"
mongo = PyMongo(app)


class FruitSchema(Schema):
  name = fields.String(required=True)
  sugar_content = fields.Integer(required=True)
  colour = fields.String(required=True)
  country = fields.String(required=True)


@app.route("/fruit", methods=["POST"])
def add_new_fruit(id):
  request_dict = request.json
  new_fruit = FruitSchema.load(request_dict)

  fruit_document = mongo.db.fruits.insert_one(new_fruit)
  fruit_id = fruit_document.inserted_id

  fruit = mongo.db.fruits.find_one({"_id": fruit_id})

  fruit_json = loads(dumps(fruit))

  return jsonify(fruit_json)


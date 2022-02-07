from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from marshmallow import Schema, fields
from bson.json_util import dumps
from json import loads
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_CONNECTION_STRING")
mongo = PyMongo(app)


class FruitSchema(Schema):
  name = fields.String(required=True)
  sugar_content = fields.Integer(required=True)
  colour = fields.String(required=True)
  calories = fields.Integer(required=True)


@app.route("/fruit", methods=["POST"])
def add_new_fruit():
  request_dict = request.json
  new_fruit = FruitSchema().load(request_dict)

  fruit_document = mongo.db.fruits.insert_one(new_fruit)
  fruit_id = fruit_document.inserted_id

  fruit = mongo.db.fruits.find_one({"_id": fruit_id})

  fruit_json = loads(dumps(fruit))

  return jsonify(fruit_json)


@app.route("/fruit", methods=["GET"])
def get_fruits():
  fruits = mongo.db.fruits.find()
  fruits_list = loads(dumps(fruits))

  return jsonify(fruits_list)


#! FIX THIS CUZ IT BREAKS
@app.route("/fruit/<ObjectId:id>", methods=["PATCH"])
def update_fruit(id):
  mongo.db.fruits.update_one({"_id": id}, {"$set": request.data })

  fruit = mongo.db.fruits.find_one(id)

  fruit_json = loads(dumps(fruit))
  return fruit_json


@app.route("/fruit/<ObjectId:id>", methods=["DELETE"])
def delete_fruit(id):
  result = mongo.db.fruits.delete_one({"_id": id})

  if result.deleted_count == 1:
    return {
      "success": True
    }
  else:
    return {
      "success": False
    }, 400


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port="3001")
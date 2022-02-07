from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://week3:1yDxm2EdXKkIwby4@cluster0.xtk0f.mongodb.net/fruit_basket?retryWrites=true&w=majority"
mongo = PyMongo(app)



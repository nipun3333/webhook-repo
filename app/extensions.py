from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)

# Setup MongoDB here
app.config['MONGO_URI'] = "mongodb://localhost:27017/database"

mongo = PyMongo(app)

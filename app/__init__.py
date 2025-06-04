from flask import Flask
from flask_pymongo import PyMongo
from config import Config
import os

mongo = PyMongo()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if os.environ.get('VERCEL'):
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

    mongo.init_app(app)
    
    return app
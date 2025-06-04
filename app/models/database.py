from flask_pymongo import PyMongo
from app import mongo

def get_db():
    return mongo.db
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
    
    from app.routes import artesao_routes, produto_routes, auth_routes
    app.register_blueprint(artesao_routes.bp)
    app.register_blueprint(produto_routes.bp)
    app.register_blueprint(auth_routes.bp)
    
    return app
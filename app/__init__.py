from flask import Flask
from flask_pymongo import PyMongo
from config import Config
import os
import time
from pymongo.errors import ConnectionFailure

mongo = PyMongo()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    if 'VERCEL' in os.environ:
        app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
    
    max_retries = 3
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            mongo.init_app(app)
            
            with app.app_context():
                time.sleep(1)
                mongo.cx.admin.command('ping')
            break
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  
            continue
    
    if last_exception is not None:
        raise RuntimeError(f"Failed to connect to MongoDB after {max_retries} attempts. Last error: {str(last_exception)}")
    
    from app.routes import artesao_routes, produto_routes, auth_routes
    app.register_blueprint(artesao_routes.bp)
    app.register_blueprint(produto_routes.bp)
    app.register_blueprint(auth_routes.bp)
    
    @app.route('/health')
    def health_check():
        try:
            mongo.cx.admin.command('ping')
            return {'status': 'healthy', 'database': 'connected'}, 200
        except ConnectionFailure:
            return {'status': 'unhealthy', 'database': 'disconnected'}, 500
    
    return app
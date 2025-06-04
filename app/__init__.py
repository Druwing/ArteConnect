from flask import Flask
from flask_pymongo import PyMongo
from config import Config
import os
import time

mongo = PyMongo()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    if 'VERCEL' in os.environ:
        app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            mongo.init_app(app)
            with app.app_context():
                mongo.db.command('ping')
            break
        except Exception as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"Failed to connect to MongoDB after {max_retries} attempts: {str(e)}")
            time.sleep(1)
    
    from app.routes import artesao_routes, produto_routes, auth_routes
    app.register_blueprint(artesao_routes.bp)
    app.register_blueprint(produto_routes.bp)
    app.register_blueprint(auth_routes.bp)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'database': 'connected'}
    
    return app

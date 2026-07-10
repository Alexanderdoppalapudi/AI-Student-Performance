"""Flask app initialization"""

from flask import Flask
from flask_cors import CORS
import logging
from .config import config

def create_app(config_name='development'):
    """Create and configure Flask app"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Register blueprints
    from .routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

"""Main entry point for the Flask application"""

import os
from api import create_app

if __name__ == '__main__':
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    port = int(os.getenv('PORT', 5000))
    debug = config_name == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

from flask import Flask
from flask_cors import CORS
from src.config import config
from src.database import init_db

def create_app(config_name='development'):
    """
    Application Factory Pattern
    
    Why?
    - Easy to create multiple app instances (testing, production)
    - Configuration happens in one place
    - Extensions initialize properly
    """
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS (allow frontend to make requests)
    CORS(app)
    
    # Initialize database and extensions
    init_db(app)
    
    # Register blueprints (routes)
    from src.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    # Health check route (to test if server is running)
    @app.route('/health', methods=['GET'])
    def health_check():
        return {
            'status': 'healthy',
            'message': 'Flask backend is running! 🚀'
        }, 200
    
    return app

# This runs when you execute: python src/app.py
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
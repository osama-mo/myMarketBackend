from flask import Flask
from flask_cors import CORS
from src.config import config
from src.database import init_db

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app)
    init_db(app)
    
    # Register blueprints
    from src.routes.auth_routes import auth_bp
    from src.routes.product_routes import product_bp
    from src.routes.basket_routes import basket_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(basket_bp)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return {
            'status': 'healthy',
            'message': 'Flask backend is running! 🚀'
        }, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
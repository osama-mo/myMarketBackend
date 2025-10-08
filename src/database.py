from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def init_db(app):
    """Initialize database and related extensions with the Flask app."""
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        # Import all models explicitly BEFORE creating tables
        # Order matters: import parent tables before child tables
        from src.models.user import User
        from src.models.product import Product
        from src.models.basket import Basket, BasketItem
        
        # Now create all tables
        db.create_all()
        print("✅ Database and tables created.")
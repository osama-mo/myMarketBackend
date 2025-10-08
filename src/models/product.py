from src.database import db
from datetime import datetime

class Product(db.Model):
    """
    Product Model - Represents a product in the marketplace
    
    Fields:
    - id: Unique identifier
    - name: Product name
    - description: Detailed description
    - price: Product price (in dollars)
    - stock: Available quantity
    - category: Product category (electronics, clothing, etc.)
    - image_url: Product image URL (optional)
    - created_by: Admin user who created the product
    - created_at: When product was added
    - updated_at: Last update timestamp
    """
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    category = db.Column(db.String(50), index=True)
    image_url = db.Column(db.String(255))
    
    # Foreign key: which admin created this product
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship: Product belongs to a user (admin)
    creator = db.relationship('User', backref='products')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category': self.category,
            'image_url': self.image_url,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def is_in_stock(self):
        """Check if product is available"""
        return self.stock > 0
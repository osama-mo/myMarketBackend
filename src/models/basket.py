from src.database import db
from datetime import datetime

class Basket(db.Model):
    """
    Basket Model - User's shopping cart
    
    Status values:
    - 'active': Current shopping cart
    - 'completed': Checked out (becomes an order)
    - 'abandoned': User left without checkout
    """
    
    __tablename__ = 'baskets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship: Basket has many items
    items = db.relationship('BasketItem', backref='basket', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Basket user_id={self.user_id} status={self.status}>'
    
    def to_dict(self):
        """Convert basket to dictionary with items"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'items': [item.to_dict() for item in self.items],
            'total_items': len(self.items),
            'total_price': self.get_total_price(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_total_price(self):
        """Calculate total price of all items in basket"""
        return sum(item.get_subtotal() for item in self.items)
    
    def is_active(self):
        """Check if basket is currently active"""
        return self.status == 'active'


class BasketItem(db.Model):
    """
    BasketItem Model - Individual product in a basket
    
    Represents the many-to-many relationship between Basket and Product
    with additional data (quantity)
    """
    
    __tablename__ = 'basket_items'
    
    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.id'), nullable=False)
    # Use string reference 'products.id' instead of importing Product
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Use string reference in relationship
    product = db.relationship('Product', backref='basket_items', lazy=True)
    
    def __repr__(self):
        return f'<BasketItem product_id={self.product_id} qty={self.quantity}>'
    
    def to_dict(self):
        """Convert basket item to dictionary"""
        return {
            'id': self.id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'subtotal': self.get_subtotal(),
            'added_at': self.added_at.isoformat()
        }
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.product.price * self.quantity if self.product else 0
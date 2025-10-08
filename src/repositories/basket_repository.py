from src.database import db
from src.models.basket import Basket, BasketItem
from src.models.product import Product

class BasketRepository:
    """
    Basket Repository - Handles all database operations for Baskets
    """
    
    @staticmethod
    def get_active_basket(user_id):
        """Get user's active basket (current shopping cart)"""
        return Basket.query.filter_by(user_id=user_id, status='active').first()
    
    @staticmethod
    def create_basket(user_id):
        """Create a new active basket for user"""
        basket = Basket(user_id=user_id, status='active')
        db.session.add(basket)
        db.session.commit()
        return basket
    
    @staticmethod
    def get_or_create_basket(user_id):
        """Get active basket or create if doesn't exist"""
        basket = BasketRepository.get_active_basket(user_id)
        if not basket:
            basket = BasketRepository.create_basket(user_id)
        return basket
    
    @staticmethod
    def add_item(basket_id, product_id, quantity=1):
        """
        Add item to basket or update quantity if already exists
        
        Returns:
            (basket_item, created) tuple
            - basket_item: The BasketItem object
            - created: True if new item, False if updated existing
        """
        # Check if item already exists in basket
        existing_item = BasketItem.query.filter_by(
            basket_id=basket_id,
            product_id=product_id
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            db.session.commit()
            return existing_item, False
        else:
            # Create new item
            item = BasketItem(
                basket_id=basket_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(item)
            db.session.commit()
            return item, True
    
    @staticmethod
    def update_item_quantity(basket_id, product_id, quantity):
        """Update quantity of item in basket"""
        item = BasketItem.query.filter_by(
            basket_id=basket_id,
            product_id=product_id
        ).first()
        
        if not item:
            return None
        
        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            db.session.delete(item)
        else:
            item.quantity = quantity
        
        db.session.commit()
        return item
    
    @staticmethod
    def remove_item(basket_id, product_id):
        """Remove item from basket"""
        item = BasketItem.query.filter_by(
            basket_id=basket_id,
            product_id=product_id
        ).first()
        
        if not item:
            return False
        
        db.session.delete(item)
        db.session.commit()
        return True
    
    @staticmethod
    def clear_basket(basket_id):
        """Remove all items from basket"""
        BasketItem.query.filter_by(basket_id=basket_id).delete()
        db.session.commit()
        return True
    
    @staticmethod
    def get_basket_by_id(basket_id):
        """Get basket by ID"""
        return Basket.query.get(basket_id)
    
    @staticmethod
    def complete_basket(basket_id):
        """Mark basket as completed (checkout)"""
        basket = Basket.query.get(basket_id)
        if basket:
            basket.status = 'completed'
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_user_baskets(user_id, status=None):
        """
        Get all baskets for a user
        
        Args:
            user_id: User ID
            status: Filter by status ('active', 'completed', 'abandoned')
        """
        query = Basket.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(Basket.created_at.desc()).all()
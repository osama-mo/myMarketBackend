from src.repositories.basket_repository import BasketRepository
from src.repositories.product_repository import ProductRepository
from src.database import db  # ← ADD THIS LINE

class BasketService:
    """
    Basket Service - Business logic for shopping cart
    """
    
    @staticmethod
    def get_basket(user):
        """
        Get user's active basket
        
        Returns:
            (basket_data, error) tuple
        """
        try:
            basket = BasketRepository.get_or_create_basket(user.id)
            return basket.to_dict(), None
        except Exception as e:
            return None, f"Error fetching basket: {str(e)}"
    
    @staticmethod
    def add_to_basket(user, product_id, quantity=1):
        """
        Add product to basket
        
        Args:
            user: Current user
            product_id: Product ID to add
            quantity: Quantity to add (default 1)
        
        Returns:
            (basket_data, error) tuple
        """
        
        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return None, "Quantity must be positive"
        except (TypeError, ValueError):
            return None, "Invalid quantity"
        
        # Check if product exists
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            return None, "Product not found"
        
        # Check stock availability
        if product.stock < quantity:
            return None, f"Not enough stock. Available: {product.stock}"
        
        # Get or create basket
        basket = BasketRepository.get_or_create_basket(user.id)
        
        # Calculate total quantity if item already in basket
        existing_item = None
        for item in basket.items:
            if item.product_id == product_id:
                existing_item = item
                break
        
        total_quantity = quantity
        if existing_item:
            total_quantity = existing_item.quantity + quantity
        
        # Check if total quantity exceeds stock
        if total_quantity > product.stock:
            return None, f"Cannot add {quantity}. Maximum available: {product.stock - (existing_item.quantity if existing_item else 0)}"
        
        # Add item to basket
        item, created = BasketRepository.add_item(basket.id, product_id, quantity)
        
        # Refresh basket to get updated data
        basket = BasketRepository.get_basket_by_id(basket.id)
        
        action = "added to" if created else "updated in"
        return {
            'basket': basket.to_dict(),
            'message': f"Product {action} basket"
        }, None
    
    @staticmethod
    def update_basket_item(user, product_id, quantity):
        """
        Update quantity of item in basket
        
        Args:
            user: Current user
            product_id: Product ID to update
            quantity: New quantity (0 to remove)
        
        Returns:
            (basket_data, error) tuple
        """
        
        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity < 0:
                return None, "Quantity cannot be negative"
        except (TypeError, ValueError):
            return None, "Invalid quantity"
        
        # Get basket
        basket = BasketRepository.get_active_basket(user.id)
        if not basket:
            return None, "Basket not found"
        
        # If quantity > 0, check stock
        if quantity > 0:
            product = ProductRepository.get_product_by_id(product_id)
            if not product:
                return None, "Product not found"
            
            if quantity > product.stock:
                return None, f"Not enough stock. Available: {product.stock}"
        
        # Update item
        item = BasketRepository.update_item_quantity(basket.id, product_id, quantity)
        if not item and quantity > 0:
            return None, "Item not found in basket"
        
        # Refresh basket
        basket = BasketRepository.get_basket_by_id(basket.id)
        
        message = "Item removed from basket" if quantity == 0 else "Item quantity updated"
        return {
            'basket': basket.to_dict(),
            'message': message
        }, None
    
    @staticmethod
    def remove_from_basket(user, product_id):
        """
        Remove product from basket
        
        Args:
            user: Current user
            product_id: Product ID to remove
        
        Returns:
            (basket_data, error) tuple
        """
        
        # Get basket
        basket = BasketRepository.get_active_basket(user.id)
        if not basket:
            return None, "Basket not found"
        
        # Remove item
        success = BasketRepository.remove_item(basket.id, product_id)
        if not success:
            return None, "Item not found in basket"
        
        # Refresh basket
        basket = BasketRepository.get_basket_by_id(basket.id)
        
        return {
            'basket': basket.to_dict(),
            'message': "Item removed from basket"
        }, None
    
    @staticmethod
    def clear_basket(user):
        """
        Clear all items from basket
        
        Returns:
            (success, error) tuple
        """
        
        # Get basket
        basket = BasketRepository.get_active_basket(user.id)
        if not basket:
            return None, "Basket not found"
        
        # Clear basket
        BasketRepository.clear_basket(basket.id)
        
        # Refresh basket
        basket = BasketRepository.get_basket_by_id(basket.id)
        
        return {
            'basket': basket.to_dict(),
            'message': "Basket cleared"
        }, None
    
    @staticmethod
    def checkout(user):
        """
        Checkout basket (mark as completed and create new active basket)
        
        Returns:
            (order_data, error) tuple
        """
        
        # Get basket
        basket = BasketRepository.get_active_basket(user.id)
        if not basket:
            return None, "Basket not found"
        
        # Check if basket has items
        if not basket.items:
            return None, "Cannot checkout empty basket"
        
        # Check stock availability for all items
        for item in basket.items:
            if item.product.stock < item.quantity:
                return None, f"Product '{item.product.name}' is out of stock. Available: {item.product.stock}"
        
        # Reduce stock for each product
        for item in basket.items:
            product = item.product
            product.stock -= item.quantity
        
        # Mark basket as completed
        BasketRepository.complete_basket(basket.id)
        
        # Create new active basket for user
        new_basket = BasketRepository.create_basket(user.id)
        
        db.session.commit()
        
        return {
            'order': basket.to_dict(),
            'message': 'Checkout successful',
            'new_basket': new_basket.to_dict()
        }, None
    
    @staticmethod
    def get_order_history(user):
        """
        Get user's completed orders
        
        Returns:
            (orders, error) tuple
        """
        try:
            orders = BasketRepository.get_user_baskets(user.id, status='completed')
            return [order.to_dict() for order in orders], None
        except Exception as e:
            return None, f"Error fetching orders: {str(e)}"
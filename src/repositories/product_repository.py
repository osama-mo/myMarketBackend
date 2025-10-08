from src.database import db
from src.models.product import Product

class ProductRepository:
    """Repository for Product model - handles DB operations"""
    

    @staticmethod
    def create_product(name, description, price, stock, category, image_url, created_by):
        """Create and save a new product"""
        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image_url=image_url,
            created_by=created_by
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product
    
    @staticmethod
    def get_product_by_id(product_id):
        """Retrieve a product by its ID"""
        return Product.query.get(product_id)
    
    @staticmethod
    def get_all_products(page=1, per_page=10 , category=None, search=None):
        """Retrieve all products with optional pagination, category filter, and search"""
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                db.or_(
                    Product.name.ilike(search_pattern),
                    Product.description.ilike(search_pattern)
                )
            )
        query = query.order_by(Product.created_at.desc())

        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def update_product(product_id, **kwargs):
        """Update product details"""
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            return None
        
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        db.session.commit()
        return product
    
    @staticmethod
    def delete_product(product_id):
        """Delete a product by its ID"""
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            return False
        
        db.session.delete(product)
        db.session.commit()
        return True
    
    @staticmethod
    def get_categories():
        """Retrieve distinct product categories"""
        categories = db.session.query(Product.category).distinct().all()
        return [c[0] for c in categories if c[0]]  # Extract category names from tuples
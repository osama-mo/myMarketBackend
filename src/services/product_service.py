from src.repositories.product_repository import ProductRepository

class ProductService:
    """
    Product Service - Business logic for product management
    """
    
    @staticmethod
    def create_product(user, name, description, price, stock, category=None, image_url=None):
        """
        Create a new product (admin only)
        """
        
        # Authorization: Only admins can create products
        if not user.is_admin():
            return None, "Only administrators can create products"
        
        # Validation
        if not name or len(str(name).strip()) < 3:
            return None, "Product name must be at least 3 characters"
        
        if not description or len(str(description).strip()) < 10:
            return None, "Product description must be at least 10 characters"
        
        # Convert and validate price
        try:
            price = float(price)
            if price < 0:
                return None, "Price must be a positive number"
        except (TypeError, ValueError):
            return None, "Price must be a valid number"
        
        # Convert and validate stock
        try:
            stock = int(stock)
            if stock < 0:
                return None, "Stock must be a non-negative number"
        except (TypeError, ValueError):
            return None, "Stock must be a valid number"
        
        # Create product
        product = ProductRepository.create_product(
            name=str(name).strip(),
            description=str(description).strip(),
            price=price,
            stock=stock,
            category=str(category).strip() if category else None,
            image_url=str(image_url).strip() if image_url else None,
            created_by=user.id
        )
        
        return product, None
    
    @staticmethod
    def get_product(product_id):
        """Get a single product by ID"""
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            return None, "Product not found"
        
        return product, None
    
    @staticmethod
    def get_products(page=1, per_page=10, category=None, search=None):
        """Get products with pagination and filters"""
        try:
            page = int(page) if page else 1
            per_page = int(per_page) if per_page else 10
            
            # Limit per_page to prevent abuse
            if per_page > 100:
                per_page = 100
            
            pagination = ProductRepository.get_all_products(
                page=page,
                per_page=per_page,
                category=category,
                search=search
            )
            
            return {
                'products': [p.to_dict() for p in pagination.items],
                'total': pagination.total,
                'page': pagination.page,
                'per_page': pagination.per_page,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }, None
            
        except Exception as e:
            return None, f"Error fetching products: {str(e)}"
    
    @staticmethod
    def update_product(user, product_id, **kwargs):
        """
        Update a product (admin only)
        """
        
        # Authorization
        if not user.is_admin():
            return None, "Only administrators can update products"
        
        # Validate price if provided
        if 'price' in kwargs:
            try:
                price = float(kwargs['price'])
                if price < 0:
                    return None, "Price must be a positive number"
                kwargs['price'] = price
            except (TypeError, ValueError):
                return None, "Price must be a valid number"
        
        # Validate stock if provided
        if 'stock' in kwargs:
            try:
                stock = int(kwargs['stock'])
                if stock < 0:
                    return None, "Stock must be a non-negative number"
                kwargs['stock'] = stock
            except (TypeError, ValueError):
                return None, "Stock must be a valid number"
        
        # Update product
        product = ProductRepository.update_product(product_id, **kwargs)
        if not product:
            return None, "Product not found"
        
        return product, None
    
    @staticmethod
    def delete_product(user, product_id):
        """
        Delete a product (admin only)
        """
        
        # Authorization
        if not user.is_admin():
            return False, "Only administrators can delete products"
        
        success = ProductRepository.delete_product(product_id)
        if not success:
            return False, "Product not found"
        
        return True, None
    
    @staticmethod
    def get_categories():
        """Get all product categories"""
        categories = ProductRepository.get_categories()
        return categories, None
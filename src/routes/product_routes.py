from flask import Blueprint, request
from src.services.product_service import ProductService
from src.utils.responses import success_response, error_response
from src.middleware.auth_middleware import jwt_required_custom

product_bp = Blueprint('products', __name__, url_prefix='/products')


@product_bp.route('', methods=['GET'])
def get_products():
    """
    Get all products with pagination and filters
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10, max: 100)
    - category: Filter by category (optional)
    - search: Search in name/description (optional)
    
    Example: GET /products?page=1&per_page=10&category=electronics&search=phone
    """
    try:
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        category = request.args.get('category')
        search = request.args.get('search')
        
        result, error = ProductService.get_products(
            page=page,
            per_page=per_page,
            category=category,
            search=search
        )
        
        if error:
            return error_response(error, 400)
        
        return success_response(data=result, message="Products retrieved successfully")
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get a single product by ID
    
    Example: GET /products/1
    """
    try:
        product, error = ProductService.get_product(product_id)
        
        if error:
            return error_response(error, 404)
        
        return success_response(
            data={'product': product.to_dict()},
            message="Product retrieved successfully"
        )
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@product_bp.route('', methods=['POST'])
@jwt_required_custom
def create_product(current_user):
    """
    Create a new product (ADMIN ONLY)
    
    Requires: Authorization header with Bearer token
    
    Request Body:
    {
        "name": "iPhone 15",
        "description": "Latest iPhone model",
        "price": 999.99,
        "stock": 50,
        "category": "electronics",
        "image_url": "https://..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("No data provided", 400)
        
        product, error = ProductService.create_product(
            user=current_user,
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            stock=data.get('stock'),
            category=data.get('category'),
            image_url=data.get('image_url')
        )
        
        if error:
            return error_response(error, 400)
        
        return success_response(
            data={'product': product.to_dict()},
            message="Product created successfully",
            status_code=201
        )
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required_custom
def update_product(current_user, product_id):
    """
    Update a product (ADMIN ONLY)
    
    Request Body: (all fields optional)
    {
        "name": "Updated name",
        "price": 899.99,
        "stock": 100
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("No data provided", 400)
        
        product, error = ProductService.update_product(
            user=current_user,
            product_id=product_id,
            **data
        )
        
        if error:
            return error_response(error, 400)
        
        return success_response(
            data={'product': product.to_dict()},
            message="Product updated successfully"
        )
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required_custom
def delete_product(current_user, product_id):
    """
    Delete a product (ADMIN ONLY)
    
    Example: DELETE /products/1
    """
    try:
        success, error = ProductService.delete_product(current_user, product_id)
        
        if error:
            return error_response(error, 400)
        
        return success_response(message="Product deleted successfully")
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@product_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all product categories
    
    Example: GET /products/categories
    """
    try:
        categories, error = ProductService.get_categories()
        
        if error:
            return error_response(error, 400)
        
        return success_response(
            data={'categories': categories},
            message="Categories retrieved successfully"
        )
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)
from flask import Blueprint, request
from src.services.basket_service import BasketService
from src.utils.responses import success_response, error_response
from src.middleware.auth_middleware import jwt_required_custom

basket_bp = Blueprint('basket', __name__, url_prefix='/basket')


@basket_bp.route('', methods=['GET'])
@jwt_required_custom
def get_basket(current_user):
    """
    Get user's active basket
    
    Response:
    {
        "basket": {
            "id": 1,
            "items": [...],
            "total_items": 3,
            "total_price": 129.97
        }
    }
    """
    try:
        result, error = BasketService.get_basket(current_user)
        
        if error:
            return error_response(error, 400)
        
        return success_response(data=result, message="Basket retrieved successfully")
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@basket_bp.route('/add', methods=['POST'])
@jwt_required_custom
def add_to_basket(current_user):
    """
    Add product to basket
    
    Request Body:
    {
        "product_id": 1,
        "quantity": 2
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("No data provided", 400)
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return error_response("Product ID is required", 400)
        
        result, error = BasketService.add_to_basket(current_user, product_id, quantity)
        
        if error:
            return error_response(error, 400)
        
        return success_response(data=result['basket'], message=result['message'])
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@basket_bp.route('/update', methods=['PUT'])
@jwt_required_custom
def update_basket_item(current_user):
    """
    Update quantity of item in basket
    
    Request Body:
    {
        "product_id": 1,
        "quantity": 5
    }
    
    Note: Set quantity to 0 to remove item
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("No data provided", 400)
        
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        
        if not product_id or quantity is None:
            return error_response("Product ID and quantity are required", 400)
        
        result, error = BasketService.update_basket_item(current_user, product_id, quantity)
        
        if error:
            return error_response(error, 400)
        
        return success_response(data=result['basket'], message=result['message'])
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@basket_bp.route('/remove/<int:product_id>', methods=['DELETE'])
@jwt_required_custom
def remove_from_basket(current_user, product_id):
    """
    Remove product from basket
    
    Example: DELETE /basket/remove/1
    """
    try:
        result, error = BasketService.remove_from_basket(current_user, product_id)
        
        if error:
            return error_response(error, 400)
        
        return success_response(data=result['basket'], message=result['message'])
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@basket_bp.route('/clear', methods=['DELETE'])
@jwt_required_custom
def clear_basket(current_user):
    """
    Clear all items from basket
    
    Example: DELETE /basket/clear
    """
    try:
        result, error = BasketService.clear_basket(current_user)
        
        if error:
            return error_response(error, 400)
        
        return success_response(data=result['basket'], message=result['message'])
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@basket_bp.route('/checkout', methods=['POST'])
@jwt_required_custom
def checkout(current_user):
    """
    Checkout basket (complete order)
    
    - Validates stock availability
    - Reduces product stock
    - Marks basket as completed
    - Creates new active basket
    
    Response:
    {
        "order": {...},
        "message": "Checkout successful",
        "new_basket": {...}
    }
    """
    try:
        result, error = BasketService.checkout(current_user)
        
        if error:
            return error_response(error, 400)
        
        return success_response(data=result, message=result['message'])
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)


@basket_bp.route('/orders', methods=['GET'])
@jwt_required_custom
def get_order_history(current_user):
    """
    Get user's order history (completed baskets)
    
    Response:
    {
        "orders": [
            {
                "id": 1,
                "status": "completed",
                "items": [...],
                "total_price": 129.97
            }
        ]
    }
    """
    try:
        orders, error = BasketService.get_order_history(current_user)
        
        if error:
            return error_response(error, 400)
        
        return success_response(
            data={'orders': orders},
            message="Order history retrieved successfully"
        )
        
    except Exception as e:
        return error_response(f"Server error: {str(e)}", 500)
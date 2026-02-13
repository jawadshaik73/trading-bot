"""
Input validators for order parameters.
"""
import re
from typing import Tuple, Optional
from config import MAX_ORDER_QUANTITY, MIN_ORDER_QUANTITY

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Validate trading symbol format.
    
    Args:
        symbol: Trading symbol (e.g., BTCUSDT)
        
    Returns:
        Validated symbol in uppercase
        
    Raises:
        ValidationError: If symbol is invalid
    """
    symbol = symbol.upper().strip()
    
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    if not re.match(r'^[A-Z0-9]{6,}$', symbol):
        raise ValidationError(
            f"Invalid symbol format: '{symbol}'. Expected format like BTCUSDT"
        )
    
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.
    
    Args:
        side: Order side (BUY or SELL)
        
    Returns:
        Validated side in uppercase
        
    Raises:
        ValidationError: If side is invalid
    """
    side = side.upper().strip()
    
    if side not in ['BUY', 'SELL']:
        raise ValidationError(
            f"Invalid side: '{side}'. Must be 'BUY' or 'SELL'"
        )
    
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.
    
    Args:
        order_type: Order type (MARKET or LIMIT)
        
    Returns:
        Validated order type in uppercase
        
    Raises:
        ValidationError: If order type is invalid
    """
    order_type = order_type.upper().strip()
    
    valid_types = ['MARKET', 'LIMIT', 'STOP_LOSS', 'TAKE_PROFIT']
    if order_type not in valid_types:
        raise ValidationError(
            f"Invalid order type: '{order_type}'. "
            f"Must be one of: {', '.join(valid_types)}"
        )
    
    return order_type


def validate_quantity(quantity: float) -> float:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity
        
    Returns:
        Validated quantity
        
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(
            f"Invalid quantity: '{quantity}'. Must be a valid number"
        )
    
    if qty <= 0:
        raise ValidationError("Quantity must be greater than 0")
    
    if qty < MIN_ORDER_QUANTITY:
        raise ValidationError(
            f"Quantity ({qty}) is below minimum ({MIN_ORDER_QUANTITY})"
        )
    
    if qty > MAX_ORDER_QUANTITY:
        raise ValidationError(
            f"Quantity ({qty}) exceeds maximum ({MAX_ORDER_QUANTITY})"
        )
    
    return qty


def validate_price(price: Optional[float]) -> Optional[float]:
    """
    Validate order price.
    
    Args:
        price: Order price (can be None for market orders)
        
    Returns:
        Validated price or None
        
    Raises:
        ValidationError: If price is invalid
    """
    if price is None:
        return None
    
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError(
            f"Invalid price: '{price}'. Must be a valid number"
        )
    
    if p <= 0:
        raise ValidationError("Price must be greater than 0")
    
    return p


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None
) -> Tuple[str, str, str, float, Optional[float]]:
    """
    Validate all order parameters together.
    
    Args:
        symbol: Trading symbol
        side: Order side (BUY/SELL)
        order_type: Order type (MARKET/LIMIT)
        quantity: Order quantity
        price: Order price (required for LIMIT)
        
    Returns:
        Tuple of validated parameters
        
    Raises:
        ValidationError: If any parameter is invalid
    """
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    
    if order_type == 'LIMIT' and price is None:
        raise ValidationError("Price is required for LIMIT orders")
    
    price = validate_price(price)
    
    return symbol, side, order_type, quantity, price

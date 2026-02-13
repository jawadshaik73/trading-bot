"""
Order placement and management logic.
"""
from typing import Dict, Any, Optional
from .client import BinanceClient, BinanceAPIError
from .validators import validate_order_params, ValidationError
from .logging_config import setup_logger

logger = setup_logger(__name__)


class OrderManager:
    """
    Manages order placement and provides high-level order operations.
    """
    
    def __init__(self, client: BinanceClient):
        """
        Initialize OrderManager.
        
        Args:
            client: BinanceClient instance
        """
        self.client = client
    
    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: float
    ) -> Dict[str, Any]:
        """
        Place a market order.
        
        Args:
            symbol: Trading symbol
            side: BUY or SELL
            quantity: Order quantity
            
        Returns:
            Order response
            
        Raises:
            ValidationError: If parameters are invalid
            BinanceAPIError: If order placement fails
        """
        try:
            symbol, side, _, quantity, _ = validate_order_params(
                symbol, side, 'MARKET', quantity
            )
            
            order_response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type='MARKET',
                quantity=quantity
            )
            
            return self._format_order_response(order_response)
        
        except (ValidationError, BinanceAPIError) as e:
            logger.error(f"Market order failed: {str(e)}")
            raise
    
    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        time_in_force: str = "GTC"
    ) -> Dict[str, Any]:
        """
        Place a limit order.
        
        Args:
            symbol: Trading symbol
            side: BUY or SELL
            quantity: Order quantity
            price: Order price
            time_in_force: Time in force (GTC, IOC, FOK)
            
        Returns:
            Order response
            
        Raises:
            ValidationError: If parameters are invalid
            BinanceAPIError: If order placement fails
        """
        try:
            symbol, side, _, quantity, price = validate_order_params(
                symbol, side, 'LIMIT', quantity, price
            )
            
            order_response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type='LIMIT',
                quantity=quantity,
                price=price,
                time_in_force=time_in_force
            )
            
            return self._format_order_response(order_response)
        
        except (ValidationError, BinanceAPIError) as e:
            logger.error(f"Limit order failed: {str(e)}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Cancellation response
            
        Raises:
            BinanceAPIError: If cancellation fails
        """
        try:
            response = self.client.cancel_order(symbol, order_id)
            logger.info(f"Order {order_id} cancelled successfully")
            return response
        except BinanceAPIError as e:
            logger.error(f"Failed to cancel order: {str(e)}")
            raise
    
    @staticmethod
    def _format_order_response(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format order response for display.
        
        Args:
            response: Raw API response
            
        Returns:
            Formatted response
        """
        return {
            'orderId': response.get('orderId'),
            'symbol': response.get('symbol'),
            'status': response.get('status'),
            'side': response.get('side'),
            'type': response.get('type'),
            'quantity': float(response.get('origQty', 0)),
            'price': float(response.get('price', 0)) if response.get('price') else None,
            'executedQty': float(response.get('executedQty', 0)),
            'cumulativeQuoteQty': float(response.get('cumQuote', 0)),
            'avgPrice': float(response.get('avgPrice', 0)) if response.get('avgPrice') else 0,
            'timeInForce': response.get('timeInForce'),
            'createTime': response.get('updateTime'),
        }
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get the status of a specific order.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Order status
            
        Raises:
            BinanceAPIError: If request fails
        """
        try:
            response = self.client.get_order(symbol, order_id)
            return self._format_order_response(response)
        except BinanceAPIError as e:
            logger.error(f"Failed to get order status: {str(e)}")
            raise

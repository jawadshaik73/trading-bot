"""
Mock Client Adapter for BinanceClient interface.
Provides a drop-in replacement for BinanceClient using MockExchange.
"""
from typing import Dict, Any, Optional
from .mock_exchange import MockExchange, MockExchangeError
from .logging_config import setup_logger

logger = setup_logger(__name__)


class MockClient:
    """
    Adapter that makes MockExchange compatible with BinanceClient interface.
    Uses the same method signatures and return format as BinanceClient.
    """
    
    def __init__(self):
        """Initialize mock client with MockExchange instance."""
        self.exchange = MockExchange()
        logger.info("MockClient initialized (offline testing mode)")
    
    def _convert_symbol(self, symbol: str) -> str:
        """
        Convert symbol from Binance format (BTCUSDT) to CCXT format (BTC/USDT).
        
        Args:
            symbol: Symbol in Binance format (e.g., BTCUSDT)
            
        Returns:
            Symbol in CCXT format (e.g., BTC/USDT)
        """
        # If already has slash, return as is
        if '/' in symbol:
            return symbol
        
        # Try to split by common patterns
        # Common quote currencies: USDT, BUSD, USDC, BTC, ETH, BNB
        quote_currencies = ['USDT', 'BUSD', 'USDC', 'BTC', 'ETH', 'BNB']
        for quote in quote_currencies:
            if symbol.endswith(quote):
                base = symbol[:-len(quote)]
                return f"{base}/{quote}"
        
        # If can't parse, assume USDT pair and insert slash before last 4 chars
        if len(symbol) > 4 and symbol[-4:].isalpha():
            return f"{symbol[:-4]}/{symbol[-4:]}"
        
        return symbol
    
    def _convert_side(self, side: str) -> str:
        """Convert side from Binance format (BUY/SELL) to lowercase (buy/sell)."""
        return side.lower()
    
    def _convert_order_type(self, order_type: str) -> str:
        """Convert order type from Binance format (MARKET/LIMIT) to lowercase."""
        return order_type.lower()
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC"
    ) -> Dict[str, Any]:
        """
        Place an order using mock exchange.
        Has the same signature as BinanceClient.place_order.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT)
            time_in_force: Time in force (GTC, IOC, FOK) - ignored in mock
            
        Returns:
            Order response in Binance API format
            
        Raises:
            MockExchangeError: If order placement fails
        """
        try:
            # Convert to mock exchange format
            mock_symbol = self._convert_symbol(symbol)
            mock_side = self._convert_side(side)
            mock_type = self._convert_order_type(order_type)
            
            logger.info(
                f"Placing {order_type} {side} order: {quantity} {symbol} @ {price or 'market'}"
            )
            
            # Create order in mock exchange
            order = self.exchange.create_order(
                symbol=mock_symbol,
                order_type=mock_type,
                side=mock_side,
                amount=quantity,
                price=price
            )
            
            # Convert response to Binance API format
            binance_order = self._format_to_binance_response(order)
            
            logger.info(f"✓ Order placed: {binance_order['orderId']}")
            return binance_order
            
        except MockExchangeError as e:
            logger.error(f"Failed to place order: {str(e)}")
            raise
    
    def get_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get order details.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Order details in Binance API format
        """
        try:
            mock_symbol = self._convert_symbol(symbol)
            order = self.exchange.fetch_order(str(order_id), mock_symbol)
            return self._format_to_binance_response(order)
        except MockExchangeError as e:
            logger.error(f"Error fetching order: {str(e)}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Cancellation response in Binance API format
        """
        try:
            mock_symbol = self._convert_symbol(symbol)
            order = self.exchange.cancel_order(str(order_id), mock_symbol)
            return self._format_to_binance_response(order)
        except MockExchangeError as e:
            logger.error(f"Error cancelling order: {str(e)}")
            raise
    
    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance.
        
        Returns:
            Account balance in Binance API format
        """
        try:
            balance = self.exchange.fetch_balance()
            
            # Convert to Binance futures account format
            return {
                'accountType': 'NORMAL',
                'maxOrders': 1000,
                'maxAlgoOrders': 200,
                'assets': [
                    {'asset': asset, 'walletBalance': str(data['total']), 'unrealizedProfit': '0'}
                    for asset, data in balance['total'].items()
                ]
            }
        except Exception as e:
            logger.error(f"Error fetching balance: {str(e)}")
            raise MockExchangeError(f"Failed to fetch balance: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test connection to mock exchange.
        
        Returns:
            True if successful
        """
        try:
            balance = self.get_account_balance()
            logger.info(f"✓ Mock connection test successful")
            logger.info(f"  Total USDT: {balance['assets'][0]['walletBalance']}")
            return True
        except Exception as e:
            logger.error(f"✗ Mock connection test failed: {e}")
            return False
    
    @staticmethod
    def _format_to_binance_response(order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert mock order to Binance API response format.
        
        Args:
            order: Order from MockExchange in CCXT format
            
        Returns:
            Order in Binance API format
        """
        # Extract symbol and convert back to no-slash format if needed
        symbol = order['symbol']
        if '/' in symbol:
            symbol = symbol.replace('/', '')
        
        return {
            'orderId': int(order['id']),
            'symbol': symbol,
            'status': order['status'].upper(),
            'side': order['side'].upper(),
            'type': order['type'].upper(),
            'origQty': str(order['amount']),
            'price': str(order['price']) if order.get('price') else '0',
            'executedQty': str(order['filled']),
            'cumulativeQuoteQty': str(order.get('cost', 0)),
            'avgPrice': str(order.get('average', 0)),
            'timeInForce': order.get('timeInForce', 'GTC') if order['type'] == 'limit' else None,
            'updateTime': order['timestamp'],
        }

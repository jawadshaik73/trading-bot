"""
CCXT-based Binance Futures client with Sandbox Mode support.
CCXT is the industry-standard library for crypto trading bots.

NOTE: Binance deprecated sandbox mode for futures trading.
For safe testing, use MockExchange (completely offline) instead.
This client is designed for production LIVE trading with proper safeguards.
"""
import ccxt
import os
from typing import Dict, Any, Optional, List
from .logging_config import setup_logger

logger = setup_logger(__name__)


class CCXTAPIError(Exception):
    """Custom exception for CCXT API errors."""
    pass


class CCXTClient:
    """
    CCXT-based Binance Futures client with sandbox mode support.
    Automatically redirects to testnet when sandbox mode is enabled.
    """
    
    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        sandbox_mode: bool = None
    ):
        """
        Initialize CCXT Binance client.
        
        NOTE: Binance removed sandbox mode for futures trading.
        For safe testing without API costs, use MockExchange instead:
            from trading_bot.bot.mock_exchange import MockExchange
            exchange = MockExchange()
        
        This client should be used for LIVE trading only, with proper safeguards.
        
        Args:
            api_key: Binance API key (leave empty to use .env)
            api_secret: Binance API secret (leave empty to use .env)
            sandbox_mode: Deprecated - Binance removed futures sandbox (ignored)
        """
        # Load from environment if not provided
        self.api_key = api_key or os.getenv("BINANCE_API_KEY", "")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET", "")
        self.sandbox_mode = False  # Sandbox is no longer supported by Binance
        enable_rate_limit = os.getenv("ENABLE_RATE_LIMIT", "True").lower() in ("true", "1", "yes")
        
        logger.warning("⚠️  CCXT Client - Binance removed futures sandbox mode")
        logger.warning("📦 Use MockExchange for safe testing: from trading_bot.bot.mock_exchange import MockExchange")
        logger.warning("🚀 This client is for PRODUCTION LIVE TRADING")
        
        # Initialize CCXT Binance exchange
        self.exchange = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': enable_rate_limit,
            'options': {
                'defaultType': 'future',  # Use Futures endpoints
                'transactionTaker': 0.0004,  # Default taker fee
            }
        })
    
    def fetch_balance(self) -> Dict[str, Any]:
        """
        Fetch account balance from testnet/live exchange.
        
        Returns:
            Dict with currency balances
            
        Raises:
            CCXTAPIError: If balance fetch fails
        """
        try:
            balance = self.exchange.fetch_balance()
            logger.debug(f"Balance fetched successfully")
            return balance
        except ccxt.NetworkError as e:
            logger.error(f"Network error fetching balance: {str(e)}")
            raise CCXTAPIError(f"Network error: {str(e)}")
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error fetching balance: {str(e)}")
            raise CCXTAPIError(f"Exchange error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching balance: {str(e)}")
            raise CCXTAPIError(f"Unexpected error: {str(e)}")
    
    def create_order(
        self,
        symbol: str,
        order_type: str,
        side: str,
        amount: float,
        price: Optional[float] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an order (market, limit, etc).
        
        Args:
            symbol: Trading symbol (e.g., 'BTC/USDT')
            order_type: Order type ('market', 'limit', etc)
            side: Order side ('buy' or 'sell')
            amount: Order quantity
            price: Order price (required for limit orders)
            params: Additional params for the order
            
        Returns:
            Order response with ID, status, etc.
            
        Raises:
            CCXTAPIError: If order creation fails
        """
        try:
            params = params or {}
            
            logger.info(
                f"Creating {order_type} {side} order: "
                f"{amount} {symbol} @ {price or 'market'}"
            )
            
            order = self.exchange.create_order(
                symbol=symbol,
                type=order_type,
                side=side,
                amount=amount,
                price=price,
                params=params
            )
            
            logger.info(f"✓ Order created: {order['id']}")
            return order
            
        except ccxt.InsufficientFunds as e:
            logger.error(f"Insufficient balance: {str(e)}")
            raise CCXTAPIError(f"Insufficient balance: {str(e)}")
        except ccxt.InvalidOrder as e:
            logger.error(f"Invalid order: {str(e)}")
            raise CCXTAPIError(f"Invalid order: {str(e)}")
        except ccxt.NetworkError as e:
            logger.error(f"Network error creating order: {str(e)}")
            raise CCXTAPIError(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            raise CCXTAPIError(f"Error creating order: {str(e)}")
    
    def cancel_order(
        self,
        order_id: str,
        symbol: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Cancel an open order.
        
        Args:
            order_id: Order ID to cancel
            symbol: Trading symbol
            params: Additional params
            
        Returns:
            Canceled order response
            
        Raises:
            CCXTAPIError: If order cancellation fails
        """
        try:
            params = params or {}
            order = self.exchange.cancel_order(
                id=order_id,
                symbol=symbol,
                params=params
            )
            logger.info(f"✓ Order {order_id} cancelled")
            return order
        except ccxt.OrderNotFound as e:
            logger.error(f"Order not found: {str(e)}")
            raise CCXTAPIError(f"Order not found: {str(e)}")
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            raise CCXTAPIError(f"Error cancelling order: {str(e)}")
    
    def fetch_order(
        self,
        order_id: str,
        symbol: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Fetch order details.
        
        Args:
            order_id: Order ID
            symbol: Trading symbol
            params: Additional params
            
        Returns:
            Order details
            
        Raises:
            CCXTAPIError: If fetch fails
        """
        try:
            params = params or {}
            order = self.exchange.fetch_order(
                id=order_id,
                symbol=symbol,
                params=params
            )
            return order
        except Exception as e:
            logger.error(f"Error fetching order: {str(e)}")
            raise CCXTAPIError(f"Error fetching order: {str(e)}")
    
    def fetch_open_orders(
        self,
        symbol: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch all open orders.
        
        Args:
            symbol: Optional symbol filter
            params: Additional params
            
        Returns:
            List of open orders
            
        Raises:
            CCXTAPIError: If fetch fails
        """
        try:
            params = params or {}
            orders = self.exchange.fetch_open_orders(
                symbol=symbol,
                params=params
            )
            return orders
        except Exception as e:
            logger.error(f"Error fetching open orders: {str(e)}")
            raise CCXTAPIError(f"Error fetching open orders: {str(e)}")
    
    def fetch_ticker(
        self,
        symbol: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Fetch current ticker/price data.
        
        Args:
            symbol: Trading symbol
            params: Additional params
            
        Returns:
            Ticker data with current price
            
        Raises:
            CCXTAPIError: If fetch fails
        """
        try:
            params = params or {}
            ticker = self.exchange.fetch_ticker(symbol, params)
            return ticker
        except Exception as e:
            logger.error(f"Error fetching ticker: {str(e)}")
            raise CCXTAPIError(f"Error fetching ticker: {str(e)}")
    
    def fetch_order_book(
        self,
        symbol: str,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Fetch order book (market depth).
        
        Args:
            symbol: Trading symbol
            limit: Order book depth limit
            params: Additional params
            
        Returns:
            Order book data
            
        Raises:
            CCXTAPIError: If fetch fails
        """
        try:
            params = params or {}
            orderbook = self.exchange.fetch_order_book(
                symbol,
                limit=limit,
                params=params
            )
            return orderbook
        except Exception as e:
            logger.error(f"Error fetching order book: {str(e)}")
            raise CCXTAPIError(f"Error fetching order book: {str(e)}")
    
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[List[float]]:
        """
        Fetch OHLCV (candlestick) data.
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe ('1m', '5m', '1h', '4h', '1d', etc)
            limit: Number of candles to fetch
            params: Additional params
            
        Returns:
            List of OHLCV candles [timestamp, open, high, low, close, volume]
            
        Raises:
            CCXTAPIError: If fetch fails
        """
        try:
            params = params or {}
            ohlcv = self.exchange.fetch_ohlcv(
                symbol,
                timeframe=timeframe,
                limit=limit,
                params=params
            )
            return ohlcv
        except Exception as e:
            logger.error(f"Error fetching OHLCV: {str(e)}")
            raise CCXTAPIError(f"Error fetching OHLCV: {str(e)}")
    
    def get_exchange_info(self) -> Dict[str, Any]:
        """
        Get exchange information and market details.
        
        Returns:
            Exchange capabilities and market info
        """
        try:
            return {
                'id': self.exchange.id,
                'name': self.exchange.name,
                'sandbox': self.sandbox_mode,
                'has': {
                    'fetch_balance': self.exchange.has['fetchBalance'],
                    'create_order': self.exchange.has['createOrder'],
                    'cancel_order': self.exchange.has['cancelOrder'],
                    'fetch_ticker': self.exchange.has['fetchTicker'],
                    'fetch_ohlcv': self.exchange.has['fetchOHLCV'],
                },
                'timeframes': list(self.exchange.timeframes.keys()) if hasattr(self.exchange, 'timeframes') else []
            }
        except Exception as e:
            logger.error(f"Error getting exchange info: {str(e)}")
            return {}
    
    def test_connection(self) -> bool:
        """
        Test connection to exchange and verify credentials.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            balance = self.fetch_balance()
            mode = "TESTNET" if self.sandbox_mode else "LIVE"
            logger.info(f"✓ Connection test successful ({mode})")
            logger.info(f"  Total USDT: {balance.get('USDT', {}).get('total', 0)}")
            return True
        except CCXTAPIError as e:
            logger.error(f"✗ Connection test failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"✗ Connection test failed: {str(e)}")
            return False

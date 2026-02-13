"""
Binance Futures Testnet API client wrapper.
"""
import time
import hmac
import hashlib
from typing import Dict, Any, Optional
import requests
from .logging_config import setup_logger
from config import BINANCE_TESTNET_BASE_URL, API_KEY, API_SECRET

logger = setup_logger(__name__)


class BinanceAPIError(Exception):
    """Custom exception for Binance API errors."""
    pass


class BinanceClient:
    """
    Wrapper for Binance Futures Testnet REST API.
    Handles authentication, request signing, and error handling.
    """
    
    def __init__(self, api_key: str = "", api_secret: str = ""):
        """
        Initialize Binance client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
        """
        self.api_key = api_key or API_KEY
        self.api_secret = api_secret or API_SECRET
        self.base_url = BINANCE_TESTNET_BASE_URL
        self.session = requests.Session()
        
        if not self.api_key or not self.api_secret:
            logger.warning(
                "API credentials not provided. "
                "Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables"
            )
    
    def _generate_signature(self, query_string: str) -> str:
        """
        Generate HMAC SHA256 signature for request.
        
        Args:
            query_string: URL-encoded query string
            
        Returns:
            HMAC SHA256 signature
        """
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        signed: bool = True
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Binance API.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint (e.g., /fapi/v1/order)
            params: Query/body parameters
            signed: Whether signature is required
            
        Returns:
            JSON response from API
            
        Raises:
            BinanceAPIError: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        params = params or {}
        
        # Add timestamp for signed requests
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            query_string = '&'.join(
                f"{k}={v}" for k, v in sorted(params.items())
            )
            params['signature'] = self._generate_signature(query_string)
        
        logger.debug(f"{method} {endpoint} - Params: {params}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = self.session.post(url, headers=headers, data=params)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers, params=params)
            else:
                raise BinanceAPIError(f"Unsupported HTTP method: {method}")
            
            # Log response
            logger.debug(f"Response Status: {response.status_code}")
            
            if response.status_code != 200:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise BinanceAPIError(error_msg)
            
            data = response.json()
            logger.debug(f"Response Data: {data}")
            
            return data
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            raise BinanceAPIError(error_msg) from e
        except ValueError as e:
            error_msg = f"Invalid JSON response: {str(e)}"
            logger.error(error_msg)
            raise BinanceAPIError(error_msg) from e
    
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
        Place an order on Binance Futures Testnet.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT)
            time_in_force: Time in force (GTC, IOC, FOK) - default GTC
            
        Returns:
            Order response from API
            
        Raises:
            BinanceAPIError: If order placement fails
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        
        if order_type == 'LIMIT':
            params['price'] = price
            params['timeInForce'] = time_in_force
        
        logger.info(
            f"Placing {order_type} {side} order: {quantity} {symbol} @ {price}"
        )
        
        try:
            response = self._request('POST', '/fapi/v1/order', params=params)
            logger.info(f"Order placed successfully: {response.get('orderId')}")
            return response
        except BinanceAPIError as e:
            logger.error(f"Failed to place order: {str(e)}")
            raise
    
    def get_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get order details.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Order details
            
        Raises:
            BinanceAPIError: If request fails
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        logger.debug(f"Fetching order {order_id} for {symbol}")
        
        return self._request('GET', '/fapi/v1/order', params=params)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Cancellation response
            
        Raises:
            BinanceAPIError: If request fails
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        logger.info(f"Cancelling order {order_id} for {symbol}")
        
        return self._request('DELETE', '/fapi/v1/order', params=params)
    
    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance information.
        
        Returns:
            Account balance details
            
        Raises:
            BinanceAPIError: If request fails
        """
        logger.debug("Fetching account balance")
        
        return self._request('GET', '/fapi/v2/account')

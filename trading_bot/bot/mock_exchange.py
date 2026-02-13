"""
Mock Exchange Service for Completely Offline Testing
This provides a mock Binance exchange that doesn't require any API calls.
Perfect for testing without internet or when you want completely predictable results.
"""
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import random
from trading_bot.bot.logging_config import setup_logger

logger = setup_logger(__name__)


class MockExchangeError(Exception):
    """Custom exception for mock exchange errors."""
    pass


class MockExchange:
    """
    Complete mock Binance exchange that mimics CCXT responses.
    Generates realistic mock data without any real API calls.
    Perfect for testing trading algorithms offline.
    """
    
    def __init__(self):
        """Initialize mock exchange with simulated data."""
        # Mock account balances
        self.balances = {
            'USDT': {'free': 10000.00, 'used': 0.00, 'total': 10000.00},
            'BTC': {'free': 0.05, 'used': 0.00, 'total': 0.05},
            'ETH': {'free': 1.5, 'used': 0.00, 'total': 1.5},
            'BNB': {'free': 10.0, 'used': 0.00, 'total': 10.0},
        }
        
        # Track orders with auto-incrementing ID
        self.orders = {}
        self.order_counter = 1000
        
        # Mock current prices (in USDT)
        self.current_prices = {
            'BTC/USDT': 45000.00,
            'ETH/USDT': 2500.00,
            'BNB/USDT': 450.00,
            'ADA/USDT': 1.20,
            'SOL/USDT': 180.00,
        }
        
        # Price history for OHLCV data
        self.price_history = self._generate_price_history()
        
        logger.info("[OK] Mock Exchange initialized (offline mode)")
    
    def _generate_price_history(self) -> Dict[str, List[List[float]]]:
        """Generate realistic mock OHLCV data."""
        history = {}
        
        for symbol, price in self.current_prices.items():
            candles = []
            current_time = int((time.time() - 3600 * 24) * 1000)  # Start 24h ago
            current_price = price * 0.95  # Start at 95% of current price
            
            for i in range(24):  # Generate 24 1-hour candles
                open_price = current_price
                close_price = current_price * random.uniform(0.98, 1.02)
                high_price = max(open_price, close_price) * random.uniform(1.00, 1.02)
                low_price = min(open_price, close_price) * random.uniform(0.98, 1.00)
                volume = random.uniform(100, 1000)
                
                candles.append([
                    current_time + (i * 3600 * 1000),
                    open_price,
                    high_price,
                    low_price,
                    close_price,
                    volume
                ])
                
                current_price = close_price
            
            history[symbol] = candles
        
        return history
    
    def fetch_balance(self) -> Dict[str, Any]:
        """
        Fetch mock account balance.
        Returns realistic balance structure matching Binance response.
        """
        logger.debug("Fetching mock balance")
        
        # Build full balance structure
        balance_data = {'free': {}, 'used': {}, 'total': {}}
        
        for symbol, amounts in self.balances.items():
            balance_data['free'][symbol] = amounts['free']
            balance_data['used'][symbol] = amounts['used']
            balance_data['total'][symbol] = amounts['total']
        
        # Add some minor currencies with zero balance
        for symbol in ['XRP', 'DOGE', 'SHIB']:
            balance_data['free'][symbol] = 0.0
            balance_data['used'][symbol] = 0.0
            balance_data['total'][symbol] = 0.0
        
        return balance_data
    
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
        Create a mock order (market or limit).
        Returns realistic order structure matching Binance response.
        """
        logger.info(f"Creating {order_type} {side} order: {amount} {symbol}")
        
        # Validate inputs
        if symbol not in self.current_prices:
            raise MockExchangeError(f"Unknown symbol: {symbol}")
        
        if order_type not in ['market', 'limit']:
            raise MockExchangeError(f"Unknown order type: {order_type}")
        
        if side not in ['buy', 'sell']:
            raise MockExchangeError(f"Unknown side: {side}")
        
        # Get order price
        if order_type == 'market' or price is None:
            order_price = self.current_prices[symbol] * (1.001 if side == 'buy' else 0.999)
            order_status = 'closed'
            filled = amount
        else:
            order_price = price
            order_status = 'open'
            filled = 0  # Limit orders start unfilled
        
        # Check balance
        base, quote = symbol.split('/')
        if side == 'buy':
            needed = amount * order_price
            if self.balances[quote]['free'] < needed:
                raise MockExchangeError(f"Insufficient {quote} balance")
            self.balances[quote]['free'] -= needed
            self.balances[quote]['used'] += needed
        else:
            if self.balances[base]['free'] < amount:
                raise MockExchangeError(f"Insufficient {base} balance")
            self.balances[base]['free'] -= amount
            self.balances[base]['used'] += amount
        
        # Create order ID
        order_id = str(self.order_counter)
        self.order_counter += 1
        
        # Create order response
        order = {
            'id': order_id,
            'clientOrderId': f'mock-{order_id}',
            'timestamp': int(time.time() * 1000),
            'datetime': datetime.utcnow().isoformat() + 'Z',
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': order_type,
            'side': side,
            'price': order_price,
            'amount': amount,
            'cost': amount * order_price,
            'average': order_price,
            'filled': filled,
            'remaining': amount - filled,
            'status': order_status,
            'fee': None,
            'trades': [],
            'info': {}
        }
        
        self.orders[order_id] = order
        logger.info(f"✓ Order {order_id} created: {side} {amount} {symbol} @ ${order_price:.2f}")
        
        return order
    
    def cancel_order(
        self,
        order_id: str,
        symbol: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Cancel a mock order.
        """
        logger.info(f"Cancelling order {order_id}")
        
        if order_id not in self.orders:
            raise MockExchangeError(f"Order not found: {order_id}")
        
        order = self.orders[order_id]
        
        if order['status'] == 'closed':
            raise MockExchangeError(f"Cannot cancel closed order: {order_id}")
        
        # Release locked balance
        base, quote = order['symbol'].split('/')
        cancelled_cost = order['remaining'] * order['price']
        
        if order['side'] == 'buy':
            self.balances[quote]['used'] -= cancelled_cost
            self.balances[quote]['free'] += cancelled_cost
        else:
            self.balances[base]['used'] -= order['remaining']
            self.balances[base]['free'] += order['remaining']
        
        order['status'] = 'canceled'
        order['remaining'] = 0
        
        logger.info(f"✓ Order {order_id} cancelled")
        return order
    
    def fetch_order(
        self,
        order_id: str,
        symbol: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Fetch mock order details."""
        if order_id not in self.orders:
            raise MockExchangeError(f"Order not found: {order_id}")
        
        return self.orders[order_id]
    
    def fetch_open_orders(
        self,
        symbol: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all open mock orders."""
        open_orders = [
            order for order in self.orders.values()
            if order['status'] == 'open'
        ]
        
        if symbol:
            open_orders = [o for o in open_orders if o['symbol'] == symbol]
        
        return open_orders
    
    def fetch_ticker(
        self,
        symbol: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Fetch mock ticker data with realistic bid/ask."""
        if symbol not in self.current_prices:
            raise MockExchangeError(f"Unknown symbol: {symbol}")
        
        price = self.current_prices[symbol]
        spread = price * 0.0005  # 0.05% spread
        
        # Simulate small price movement
        price *= random.uniform(0.9995, 1.0005)
        self.current_prices[symbol] = price
        
        return {
            'symbol': symbol,
            'timestamp': int(time.time() * 1000),
            'datetime': datetime.utcnow().isoformat() + 'Z',
            'high': price * 1.02,
            'low': price * 0.98,
            'bid': price - spread,
            'bidVolume': random.uniform(100, 1000),
            'ask': price + spread,
            'askVolume': random.uniform(100, 1000),
            'vwap': price,
            'open': price * 0.98,
            'close': price,
            'last': price,
            'previousClose': price * 0.99,
            'change': price - (price * 0.99),
            'percentage': 1.0,
            'average': price,
            'baseVolume': random.uniform(1000, 10000),
            'quoteVolume': random.uniform(50000, 500000),
            'info': {}
        }
    
    def fetch_order_book(
        self,
        symbol: str,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Fetch mock order book."""
        if symbol not in self.current_prices:
            raise MockExchangeError(f"Unknown symbol: {symbol}")
        
        price = self.current_prices[symbol]
        limit = limit or 20
        
        # Generate realistic bid/ask orders
        bids = []
        asks = []
        
        for i in range(limit):
            bid_price = price * (1 - 0.0001 * (i + 1))
            ask_price = price * (1 + 0.0001 * (i + 1))
            
            bids.append([bid_price, random.uniform(0.1, 10)])
            asks.append([ask_price, random.uniform(0.1, 10)])
        
        return {
            'symbol': symbol,
            'bids': sorted(bids, reverse=True),
            'asks': sorted(asks),
            'timestamp': int(time.time() * 1000),
            'datetime': datetime.utcnow().isoformat() + 'Z',
            'nonce': int(time.time() * 1000),
        }
    
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[List[float]]:
        """Fetch mock OHLCV candlestick data."""
        if symbol not in self.current_prices:
            raise MockExchangeError(f"Unknown symbol: {symbol}")
        
        candles = self.price_history.get(symbol, [])
        
        if limit:
            candles = candles[-limit:]
        
        return candles
    
    def test_connection(self) -> bool:
        """Test mock exchange connection."""
        try:
            balance = self.fetch_balance()
            logger.info(f"✓ Mock exchange connection successful")
            logger.info(f"  Total USDT: {balance['total'].get('USDT', 0)}")
            return True
        except Exception as e:
            logger.error(f"✗ Mock exchange connection failed: {e}")
            return False


# ============================================================================
# Convenience Function: Create Mock Exchange
# ============================================================================
def create_mock_exchange() -> MockExchange:
    """
    Factory function to create a mock exchange instance.
    
    Returns:
        MockExchange instance
    """
    return MockExchange()


if __name__ == "__main__":
    # Quick test
    exchange = MockExchange()
    
    print("\n" + "="*70)
    print("Mock Exchange Test")
    print("="*70)
    
    # Test balance
    print("\n1. Fetching balance...")
    balance = exchange.fetch_balance()
    print(f"   USDT: {balance['total']['USDT']}")
    print(f"   BTC: {balance['total']['BTC']}")
    
    # Test ticker
    print("\n2. Fetching ticker...")
    ticker = exchange.fetch_ticker('BTC/USDT')
    print(f"   BTC/USDT: ${ticker['last']:.2f}")
    
    # Test order
    print("\n3. Creating market order...")
    order = exchange.create_order('BTC/USDT', 'market', 'buy', 0.01)
    print(f"   Order ID: {order['id']}")
    print(f"   Status: {order['status']}")
    
    # Test open orders
    print("\n4. Fetching open orders...")
    open_orders = exchange.fetch_open_orders()
    print(f"   Open orders: {len(open_orders)}")
    
    print("\n✓ Mock exchange tests completed!\n")

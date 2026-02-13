"""
Example: Using CCXT & Mock Exchange for Safe Testing
This demonstrates both approaches:
1. MockExchange - Completely offline, no API calls (RECOMMENDED FOR TESTING)
2. CCXTClient - For live trading with real Binance API
"""
from trading_bot.bot.mock_exchange import MockExchange
from trading_bot.bot import CCXTClient, CCXTAPIError

# ============================================================================
# EXAMPLE 1: Mock Exchange Connection Test (RECOMMENDED)
# ============================================================================
def example_mock_connection():
    """
    Connect to mock exchange - completely offline, no API calls.
    PERFECT for testing without any internet or API cost!
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Mock Exchange Connection Test (OFFLINE ✓)")
    print("="*70)
    
    exchange = MockExchange()
    
    if exchange.test_connection():
        print("✓ Mock exchange connected (completely offline)")
        
        balance = exchange.fetch_balance()
        print(f"\nMock Account Balance:")
        print(f"  USDT: ${balance['total']['USDT']:.2f}")
        print(f"  BTC: {balance['total']['BTC']:.4f}")
        print(f"  ETH: {balance['total']['ETH']:.4f}")


# ============================================================================
# EXAMPLE 2: Fetch Balance from Mock Exchange
# ============================================================================
def example_mock_fetch_balance():
    """
    Fetch account balance from mock exchange.
    This is completely predictable - perfect for testing!
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Fetch Mock Account Balance")
    print("="*70)
    
    exchange = MockExchange()
    balance = exchange.fetch_balance()
    
    print("\nMock Account Balance:")
    print("-" * 40)
    
    for symbol in ['USDT', 'BTC', 'ETH', 'BNB']:
        if symbol in balance['total']:
            free = balance['free'][symbol]
            used = balance['used'][symbol]
            total = balance['total'][symbol]
            print(f"{symbol:6} | Free: {free:12.8f} | Used: {used:12.8f}")


# ============================================================================
# EXAMPLE 3: Create a Mock Market Order
# ============================================================================
def example_mock_market_order():
    """
    Create a market order in mock exchange (instant execution).
    Perfect for testing order logic without risks!
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Create Mock Market Order (Instant ✓)")
    print("="*70)
    
    exchange = MockExchange()
    
    try:
        # Buy BTC with USDT
        order = exchange.create_order(
            symbol='BTC/USDT',
            order_type='market',
            side='buy',
            amount=0.01
        )
        
        print(f"\n✓ Market Order Created")
        print(f"  Order ID: {order['id']}")
        print(f"  Symbol: {order['symbol']}")
        print(f"  Side: {order['side'].upper()}")
        print(f"  Amount: {order['amount']} BTC")
        print(f"  Price: ${order['price']:.2f}")
        print(f"  Status: {order['status']}")
        print(f"\n  → Execution time: INSTANT (no API delays)")
    
    except Exception as e:
        print(f"✗ Error: {e}")


# ============================================================================
# EXAMPLE 4: Create a Mock Limit Order
# ============================================================================
def example_mock_limit_order():
    """
    Create a limit order in mock exchange.
    Test pending orders and cancellation logic!
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Create Mock Limit Order (Pending)")
    print("="*70)
    
    exchange = MockExchange()
    
    try:
        # Place ETH buy limit order
        order = exchange.create_order(
            symbol='ETH/USDT',
            order_type='limit',
            side='buy',
            amount=1.0,
            price=1500.0
        )
        
        print(f"\n✓ Limit Order Created")
        print(f"  Order ID: {order['id']}")
        print(f"  Symbol: {order['symbol']}")
        print(f"  Side: {order['side'].upper()}")
        print(f"  Amount: {order['amount']} ETH")
        print(f"  Price: ${order['price']:.2f}")
        print(f"  Status: {order['status']}")
        print(f"\n  → This order remains OPEN until filled or cancelled")
    
    except Exception as e:
        print(f"✗ Error: {e}")


# ============================================================================
# EXAMPLE 5: Cancel a Mock Order
# ============================================================================
def example_mock_cancel_order():
    """
    Create and then cancel a limit order.
    Test order lifecycle management!
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Create & Cancel Mock Order")
    print("="*70)
    
    exchange = MockExchange()
    
    try:
        # Create order
        order = exchange.create_order(
            symbol='BNB/USDT',
            order_type='limit',
            side='sell',
            amount=5.0,
            price=500.0
        )
        order_id = order['id']
        print(f"\n1. Created order: {order_id}")
        print(f"   Status: {order['status']}")
        
        # Cancel it
        cancelled = exchange.cancel_order(order_id, 'BNB/USDT')
        print(f"\n2. Cancelled order: {order_id}")
        print(f"   Status: {cancelled['status']}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


# ============================================================================
# EXAMPLE 6: Fetch Current Market Prices
# ============================================================================
def example_mock_fetch_ticker():
    """
    Fetch current ticker (price) data from mock exchange.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Fetch Mock Market Prices")
    print("="*70)
    
    exchange = MockExchange()
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    
    print("\nCurrent Mock Prices:")
    print("-" * 60)
    
    for symbol in symbols:
        ticker = exchange.fetch_ticker(symbol)
        print(f"{symbol:10} | Bid: ${ticker['bid']:12,.2f} | Ask: ${ticker['ask']:12,.2f}")


# ============================================================================
# EXAMPLE 7: Fetch OHLCV Candlestick Data
# ============================================================================
def example_mock_fetch_ohlcv():
    """
    Fetch OHLCV (candlestick) data for technical analysis.
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Fetch Mock OHLCV Candlestick Data")
    print("="*70)
    
    exchange = MockExchange()
    
    # Fetch pre-generated 1-hour candles
    candles = exchange.fetch_ohlcv(
        symbol='BTC/USDT',
        timeframe='1h',
        limit=5
    )
    
    print(f"\nBTC/USDT - Last 5 1H Candles:")
    print("-" * 80)
    print(f"{'Time':<12} | {'Open':>10} | {'High':>10} | {'Low':>10} | {'Close':>10}")
    print("-" * 80)
    
    from datetime import datetime
    for candle in candles:
        timestamp = datetime.fromtimestamp(candle[0]/1000).strftime('%H:%M:%S')
        open_p, high, low, close = candle[1:5]
        print(f"{timestamp:<12} | {open_p:>10.2f} | {high:>10.2f} | {low:>10.2f} | {close:>10.2f}")


# ============================================================================
# EXAMPLE 8: Mock vs Live Comparison
# ============================================================================
def example_mock_vs_live():
    """
    Comparison of mock exchange vs live trading.
    """
    print("\n" + "="*70)
    print("MOCK EXCHANGE vs LIVE CCXT CLIENT")
    print("="*70)
    
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║              MOCK EXCHANGE (RECOMMENDED FOR TESTING)           ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print("║ ✓ No API calls (completely offline)                           ║")
    print("║ ✓ Zero API costs                                               ║")
    print("║ ✓ Instant order execution                                     ║")
    print("║ ✓ Predictable test data                                       ║")
    print("║ ✓ Perfect for development & testing                          ║")
    print("║ ✓ No internet required                                         ║")
    print("║                                                                ║")
    print("║ Usage:                                                          ║")
    print("║   from trading_bot.bot.mock_exchange import MockExchange      ║")
    print("║   exchange = MockExchange()                                   ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║           LIVE CCXT CLIENT (FOR PRODUCTION TRADING)            ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print("║ ⚠ Real Binance API calls                                        ║")
    print("║ ⚠ Real money traded                                            ║")
    print("║ ⚠ Requires valid API keys                                      ║")
    print("║ ⚠ Subject to Binance rate limits                              ║")
    print("║ ⚠ Use only after extensive testing                           ║")
    print("║ ⚠ Requires proper safeguards & monitoring                    ║")
    print("║                                                                ║")
    print("║ Usage:                                                          ║")
    print("║   from trading_bot.bot import CCXTClient                      ║")
    print("║   client = CCXTClient()  # Uses BINANCE_API_KEY from .env    ║")
    print("╚════════════════════════════════════════════════════════════════╝")


# ============================================================================
# TESTING STRATEGY RECOMMENDATION
# ============================================================================
def show_testing_pipeline():
    """
    Recommended pipeline for safe bot development.
    """
    print("\n" + "="*70)
    print("RECOMMENDED TESTING PIPELINE")
    print("="*70)
    
    print("""
Step 1: UNIT TEST with MockExchange
  - Test order placement logic
  - Test balance updates
  - Test error handling
  - No API calls, instant feedback

Step 2: INTEGRATION TEST with MockExchange
  - Test strategy execution
  - Test signal generation
  - Test portfolio tracking
  - Still completely offline

Step 3: PAPER TRADING with Live API (Future)
  - Connect to real Binance API
  - Send orders but with read-only permissions first
  - Monitor for 24+ hours
  - Verify all data flows correctly

Step 4: LIVE TRADING (After All Tests Pass)
  - Start with SMALL order sizes
  - Monitor continuously
  - Have kill-switch ready
  - Scale up gradually
    """)

# ============================================================================
# Main Entry Point
# ============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("MOCK EXCHANGE & CCXT - TRADING BOT EXAMPLES")
    print("="*70)
    
    show_testing_pipeline()
    
    # Run all mock exchange examples
    example_mock_connection()
    example_mock_fetch_balance()
    example_mock_fetch_ticker()
    example_mock_fetch_ohlcv()
    example_mock_market_order()
    example_mock_limit_order()
    example_mock_cancel_order()
    example_mock_vs_live()
    
    print("\n" + "="*70)
    print("Examples completed! [check mark]")
    print("="*70)
    print("\nKey Takeaways:")
    print("• MockExchange = Perfect for testing (no API calls, completely offline)")
    print("• Use MockExchange for all development & testing")
    print("• Only use CCXTClient when you're ready for LIVE trading")
    print("• Always start with small live orders after extensive mock testing")
    print("• Monitor logs and have kill-switch ready")
    print("="*70 + "\n")

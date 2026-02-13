# CCXT Sandbox Mode Integration

## Overview

This trading bot now supports **CCXT (CryptoCurrency eXchange Trading Library)** with built-in sandbox mode. This provides a professional, industry-standard way to:

- ✅ Test trading strategies safely on testnet
- ✅ Avoid real API calls and keep credentials secure
- ✅ Use mock exchange data entirely offline
- ✅ Maintain the same API interface across all tests

---

## Quick Start: Three Deployment Options

### Option 1: CCXT Sandbox Mode (Testnet - Recommended)

The fastest way to get started with zero risk:

```python
from trading_bot.bot import CCXTClient

# Create client - sandbox mode enabled by default
client = CCXTClient(sandbox_mode=True)

# Test connection to Binance Futures Testnet
if client.test_connection():
    print("✓ Connected to testnet!")

# Fetch mock balance
balance = client.fetch_balance()
print(f"USDT: ${balance['total']['USDT']}")

# Create a simulated order (no real money)
order = client.create_order(
    symbol='BTC/USDT',
    order_type='market',
    side='buy',
    amount=0.01
)
```

**Benefits:**
- Uses Binance Futures Testnet
- CCXT automatically handles all sandbox redirects
- Realistic API responses
- Perfect for strategy testing
- **Zero financial risk**

---

### Option 2: Mock Exchange (Completely Offline)

No internet required. Completely predictable data:

```python
from trading_bot.bot.mock_exchange import MockExchange

# Create offline mock exchange
exchange = MockExchange()

# Fetch balance (zero API calls)
balance = exchange.fetch_balance()
print(f"Mock USDT: ${balance['total']['USDT']}")

# Create orders (instantly, no delays)
order = exchange.create_order(
    symbol='ETH/USDT',
    order_type='limit',
    side='buy',
    amount=1.0,
    price=2000.0
)

# Fetch OHLCV data (pre-generated)
candles = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h')
```

**Benefits:**
- Zero API calls
- No internet required
- Instant operations
- Perfect for algorithm testing
- Completely deterministic

---

### Option 3: Live Mode (Real Trading)

⚠️ **WARNING: Only use after extensive testing!**

```python
from trading_bot.bot import CCXTClient

# Create client in LIVE mode
client = CCXTClient(sandbox_mode=False)

# Real orders will be placed on Binance
order = client.create_order(
    symbol='BTC/USDT',
    order_type='market',
    side='buy',
    amount=0.01
)
```

---

## Configuration

### Environment Variables (.env)

```bash
# Your Binance API credentials
BINANCE_API_KEY=your_testnet_key_here
BINANCE_API_SECRET=your_testnet_secret_here

# Enable/Disable Sandbox Mode
# Set to True = TESTNET (safe, recommended)
# Set to False = LIVE (real money, use with caution!)
CCXT_SANDBOX_MODE=True
```

**Default:** `CCXT_SANDBOX_MODE=True` - Always starts in sandbox mode

---

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `ccxt==4.0.0` - Crypto exchange library
- Plus all other dependencies

### 2. Setup Your .env File

At the repository root, create `.env`:

```bash
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
CCXT_SANDBOX_MODE=True
```

### 3. Get Testnet Credentials (Optional)

If you want to use real Binance testnet credentials:

1. Go to https://testnet.binancefuture.com
2. Create an account
3. Generate API Key & Secret
4. Add to `.env` as shown above

---

## API Reference: CCXTClient

### Initialization

```python
from trading_bot.bot import CCXTClient

# Sandbox mode (testnet)
client = CCXTClient(sandbox_mode=True)

# Live mode (real trading)
client = CCXTClient(sandbox_mode=False)
```

### Core Methods

#### `fetch_balance()`
Get account balance

```python
balance = client.fetch_balance()

# Access balances
print(balance['total']['USDT'])  # Total USDT
print(balance['free']['BTC'])    # Available BTC
print(balance['used']['ETH'])    # Locked ETH
```

#### `create_order()`
Place a market or limit order

```python
# Market order
order = client.create_order(
    symbol='BTC/USDT',
    order_type='market',
    side='buy',
    amount=0.01
)

# Limit order
order = client.create_order(
    symbol='ETH/USDT',
    order_type='limit',
    side='sell',
    amount=1.0,
    price=3000.0
)
```

#### `cancel_order()`
Cancel an open order

```python
result = client.cancel_order(
    order_id='12345',
    symbol='BTC/USDT'
)
```

#### `fetch_order()`
Get order details

```python
order = client.fetch_order(
    order_id='12345',
    symbol='BTC/USDT'
)
```

#### `fetch_open_orders()`
Get all open orders

```python
orders = client.fetch_open_orders()
# Optional: filter by symbol
orders = client.fetch_open_orders(symbol='BTC/USDT')
```

#### `fetch_ticker()`
Get current price data

```python
ticker = client.fetch_ticker('BTC/USDT')
print(f"Bid: ${ticker['bid']}")
print(f"Ask: ${ticker['ask']}")
print(f"Last: ${ticker['last']}")
```

#### `fetch_order_book()`
Get market depth

```python
book = client.fetch_order_book('BTC/USDT', limit=20)
print(f"Bids: {book['bids']}")  # Sell orders
print(f"Asks: {book['asks']}")  # Buy orders
```

#### `fetch_ohlcv()`
Get candlestick data for technical analysis

```python
# 1-hour candles, last 100
candles = client.fetch_ohlcv(
    symbol='BTC/USDT',
    timeframe='1h',
    limit=100
)

# Each candle: [timestamp, open, high, low, close, volume]
for candle in candles:
    timestamp, open_, high, low, close, volume = candle
    print(f"Close: ${close}")
```

**Available timeframes:** '1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M'

#### `test_connection()`
Verify connection to exchange

```python
if client.test_connection():
    print("✓ Connected successfully!")
    balance = client.fetch_balance()
else:
    print("✗ Connection failed!")
```

---

## API Reference: MockExchange

For completely offline testing:

```python
from trading_bot.bot.mock_exchange import MockExchange

exchange = MockExchange()

# All methods same as CCXTClient above
balance = exchange.fetch_balance()
order = exchange.create_order('BTC/USDT', 'market', 'buy', 0.01)
ticker = exchange.fetch_ticker('ETH/USDT')
```

---

## Running Examples

### Example 1: Connection Test
```bash
python -c "
from trading_bot.bot import CCXTClient
client = CCXTClient()
client.test_connection()
"
```

### Example 2: Full Examples Suite
```bash
python examples_ccxt_sandbox.py
```

This runs comprehensive examples for:
- Sandbox connection
- Fetching balances
- Market orders
- Limit orders
- Technical analysis (OHLCV)

### Example 3: Mock Exchange Test
```bash
python -c "
from trading_bot.bot.mock_exchange import MockExchange
exchange = MockExchange()
exchange.test_connection()
balance = exchange.fetch_balance()
print(f'Mock USDT: {balance[\"total\"][\"USDT\"]}')
"
```

---

## Comparison: Legacy vs CCXT

| Feature | Legacy BinanceClient | CCXT Sandbox |
|---------|----------------------|--------------|
| Library | Manual REST API | Industry-standard CCXT |
| Sandbox Support | Manual testnet URLs | Built-in `set_sandbox_mode()` |
| Error Handling | Custom | CCXT standard exceptions |
| API Coverage | Binance only | 100+ exchanges |
| Maintenance | Manual | Community-maintained |
| Security | HMAC signing | Proven crypto library |
| Testing | Testnet only | Testnet + Mock |

---

## Migration Guide: Legacy → CCXT

### Before (Legacy)
```python
from trading_bot.bot import BinanceClient

client = BinanceClient(
    api_key=os.getenv('BINANCE_API_KEY'),
    api_secret=os.getenv('BINANCE_API_SECRET')
)

order = client.place_order(
    symbol='BTCUSDT',
    side='BUY',
    order_type='MARKET',
    quantity=0.01
)
```

### After (CCXT)
```python
from trading_bot.bot import CCXTClient

client = CCXTClient(sandbox_mode=True)

order = client.create_order(
    symbol='BTC/USDT',
    order_type='market',
    side='buy',
    amount=0.01
)
```

**Key Changes:**
- `CCXTClient` instead of `BinanceClient`
- Manual `place_order()` → `create_order()`
- Symbol format: `BTCUSDT` → `BTC/USDT`
- `quantity` → `amount`
- Automatic sandbox mode via config

---

## Important: Security Best Practices

1. **Never commit `.env` files**
   ```bash
   # Ensure .env is in .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use testnet keys for testing**
   - Get testnet-only keys
   - Zero risk even if leaked

3. **Rotate keys regularly**
   - Create new API keys quarterly
   - Revoke old keys

4. **Principle of Least Privilege**
   - Use read-only keys when possible
   - Restrict IP addresses
   - Limit order types

5. **Test thoroughly before going live**
   - Start with small orders
   - Monitor first trades manually
   - Have kill-switch ready

---

## Troubleshooting

### "Connection test failed"

**Check:**
1. `.env` file exists with correct credentials
2. Internet connection is active
3. API keys are valid (check Binance website)
4. Credentials are for testnet (not live)

### "Insufficient balance"

**In sandbox mode:**
- Mock balance is pre-set
- Edit testnet settings in Binance

**Tips:**
- Start with smaller order amounts
- Use mock exchange for unlimited testing

### "Order rejected"

**Check:**
1. Symbol format: `BTC/USDT` not `BTCUSDT`
2. Amount meets exchange minimums
3. Price is reasonable for limit orders

---

## Production Deployment Checklist

- [ ] All strategies tested extensively in sandbox
- [ ] Error handling verified
- [ ] Limits set appropriately
- [ ] Monitoring/alerts configured
- [ ] Kill-switch implemented
- [ ] Dry-run for 24 hours first
- [ ] Start with small position sizes
- [ ] Monitor logs continuously
- [ ] Have manual override ready

---

## Resources

- **CCXT Docs:** https://docs.ccxt.com/
- **Binance Testnet:** https://testnet.binancefuture.com
- **Binance API Docs:** https://binance-docs.github.io/apidocs/
- **CCXT GitHub:** https://github.com/ccxt/ccxt

---

## Support

Encountering issues? Check:

1. Example files: `examples_ccxt_sandbox.py`
2. Logs: `logs/` directory
3. Sandbox mode status in connection test output
4. CCXT documentation for exchange-specific issues

---

## License

See main repository license.

---

**Last Updated:** February 13, 2026
**Status:** Production Ready ✓

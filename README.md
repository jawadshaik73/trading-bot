# 🤖 Binance Futures Testnet Trading Bot

A professional-grade Python application for placing orders on **Binance Futures Testnet (USDT-M)** with clean code architecture, comprehensive error handling, and detailed logging.

## Features

✨ **Core Features**
- 📊 **Market Orders**: Execute immediate orders at market price
- 💰 **Limit Orders**: Place orders at specific price levels
- 🔍 **Order Status**: Check order status and details
- ❌ **Order Cancellation**: Cancel open orders
- 📈 **Account Info**: View account balance and positions
- 🧪 **API Testing**: Test connection and credentials

✅ **Professional Quality**
- Clean, modular code structure
- Comprehensive input validation
- Detailed logging to files and console
- Robust error handling
- Typing support throughout
- Beautiful CLI with colored output

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- pip package manager
- Binance Futures Testnet account

### 2. Register for Testnet

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Create a testnet account (separate from main account)
3. Complete verification
4. Generate API Key and API Secret

### 3. Installation

```bash
# Clone or extract the repository
cd trading-bot

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration

Create a `.env` file in the project root:

```bash
# .env file
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

### 5. Verify Setup

Test your API credentials:

```bash
python cli.py test
```

You should see:
```
✓ CONNECTION SUCCESSFUL
✓ API credentials are valid and connection is working
```

## Usage Examples

### Place a Market Order

```bash
python cli.py market
```

This will prompt you for:
- Trading symbol (e.g., BTCUSDT)
- Order side (BUY or SELL)
- Quantity

**Example Interactive Session:**
```
Trading symbol (e.g., BTCUSDT): BTCUSDT
Order side [BUY/SELL]: BUY
Quantity: 0.01

Order Summary:
Symbol      BTCUSDT
Side        BUY
Type        MARKET
Quantity    0.01

Execute this order? [Y/n]: y

✓ ORDER PLACED SUCCESSFULLY
Order ID        12345678
Status          FILLED
Avg Price       45000.12
Quantity        0.01
```

### Place a Limit Order

```bash
python cli.py limit
```

Example:
```
Trading symbol (e.g., BTCUSDT): ETHUSDT
Order side [BUY/SELL]: SELL
Quantity: 0.5
Limit price: 3000.00
```

### Check Order Status

```bash
python cli.py status --symbol BTCUSDT --order-id 12345678
```

### Cancel an Order

```bash
python cli.py cancel --symbol BTCUSDT --order-id 12345678
```

### View Account Information

```bash
python cli.py info
```

Shows:
- Account type
- Wallet balances
- Unrealized P&L

### Get Help

```bash
# Show all available commands
python cli.py --help

# Get help for specific command
python cli.py market --help
python cli.py limit --help
```

## Project Structure

```
trading-bot/
├── trading_bot/
│   ├── __init__.py
│   └── bot/
│       ├── __init__.py
│       ├── client.py              # Binance API client wrapper
│       ├── orders.py              # Order management logic
│       ├── validators.py          # Input validation
│       └── logging_config.py      # Logging configuration
├── cli.py                         # CLI entry point
├── config.py                      # Configuration & credentials
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (create this)
├── .env.example                  # Example env file
├── README.md                     # This file
└── logs/                         # Log files (created automatically)
    ├── cli.log
    ├── trading_bot.bot.client.log
    ├── trading_bot.bot.orders.log
    └── trading_bot.bot.validators.log
```

## Code Architecture

### Separation of Concerns

1. **`client.py`** - Low-level Binance API interaction
   - HTTP requests with HMAC-SHA256 signing
   - Error handling and logging
   - No business logic

2. **`orders.py`** - High-level order operations
   - Order placement and management
   - Response formatting
   - Order-specific validation

3. **`validators.py`** - Input validation
   - Symbol validation
   - Quantity and price validation
   - Side and order type validation

4. **`cli.py`** - User interface
   - Command routing
   - User prompts and confirmations
   - Output formatting with colors

5. **`config.py`** - Configuration management
   - API credentials (from .env)
   - Testnet URLs
   - Trading limits

## Logging

Logs are automatically saved to the `logs/` directory:

```
logs/
├── cli.log                             # CLI operations
├── trading_bot_bot_client.log          # API calls & responses
├── trading_bot_bot_orders.log          # Order operations
└── trading_bot_bot_validators.log      # Validation errors
```

Example log entries:

```
2026-02-13 14:23:45 - trading_bot.bot.client - INFO - Placing MARKET BUY order: 0.01 BTCUSDT @ None
2026-02-13 14:23:46 - trading_bot.bot.client - INFO - Order placed successfully: 12345678
2026-02-13 14:23:46 - cli - INFO - Market order placed: 12345678
```

**Log Levels:**
- `DEBUG` - Detailed API request/response info (file only)
- `INFO` - Order placements, successful operations (file & console)
- `ERROR` - Failures and exceptions (file & console)

## Error Handling

The application handles various error scenarios:

### Validation Errors
```python
# Invalid quantity
# Output: Validation Error: Quantity must be greater than 0

# Invalid symbol
# Output: Validation Error: Invalid symbol format: 'BTC'
```

### API Errors
```python
# Network connectivity issues
# Output: API Error: Network error: [connection error details]

# Invalid API credentials
# Output: API Error: HTTP 401: [error response]

# Insufficient balance
# Output: API Error: HTTP 400: [insufficient balance error]
```

### Exception Handling
All commands wrap operations in try-except blocks with user-friendly error messages.

## Configuration Options

Edit `config.py` to customize:

```python
# Testnet URL
BINANCE_TESTNET_BASE_URL = "https://testnet.binancefuture.com"

# Logging
LOG_DIR = "logs"
LOG_LEVEL = "INFO"

# Safety limits
MAX_ORDER_QUANTITY = 1000
MIN_ORDER_QUANTITY = 0.001
```

## API Reference

### BinanceClient

```python
from trading_bot.bot import BinanceClient

client = BinanceClient(api_key="xxx", api_secret="yyy")

# Place order
order = client.place_order(
    symbol="BTCUSDT",
    side="BUY",
    order_type="LIMIT",
    quantity=0.01,
    price=45000.00
)

# Get order status
order_details = client.get_order(symbol="BTCUSDT", order_id=12345)

# Cancel order
response = client.cancel_order(symbol="BTCUSDT", order_id=12345)

# Get account balance
account = client.get_account_balance()
```

### OrderManager

```python
from trading_bot.bot import BinanceClient, OrderManager

client = BinanceClient()
manager = OrderManager(client)

# Place market order
response = manager.place_market_order(
    symbol="BTCUSDT",
    side="BUY",
    quantity=0.01
)

# Place limit order
response = manager.place_limit_order(
    symbol="ETHUSDT",
    side="SELL",
    quantity=0.5,
    price=3000.00,
    time_in_force="GTC"  # Good Till Cancel
)

# Check status
status = manager.get_order_status(symbol="BTCUSDT", order_id=12345)

# Cancel
response = manager.cancel_order(symbol="BTCUSDT", order_id=12345)
```

## Testing Guide

### 1. Test API Connection

```bash
python cli.py test
```

### 2. Place Test Orders

With small quantities (use testnet only!):

```bash
# Test market order
python cli.py market --symbol BTCUSDT --side BUY --quantity 0.001

# Test limit order  
python cli.py limit --symbol ETHUSDT --side SELL --quantity 0.01 --price 1000
```

### 3. Check Logs

```bash
# View recent activity
tail -f logs/cli.log
tail -f logs/trading_bot_bot_client.log
```

### 4. Verify on Web UI

1. Log into [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Navigate to **Orders** section
3. Verify your placed orders appear there

## Troubleshooting

### "API credentials not provided"

**Solution:** Ensure `.env` file exists with:
```
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
```

Then restart the application.

### "HTTP 401: Invalid API key"

**Solution:** 
1. Verify API key and secret in `.env`
2. Ensure credentials are generated from testnet account
3. Check that API key is enabled

### "Insufficient Balance"

**Solution:**
1. Go to [Testnet Faucet](https://testnet.binancefuture.com/): "Account" → "Deposit"
2. Request faucet funds
3. Wait for confirmation
4. Retry order

### "Network error: Connection timeout"

**Solution:**
1. Check internet connection
2. Verify testnet URL is correct (should be `testnet.binancefuture.com`)
3. Try again in a few seconds

### Orders not appearing

**Solution:**
1. Check logs: `tail logs/cli.log`
2. Verify symbol exists (e.g., BTCUSDT, ETHUSDT)
3. Check order status with: `python cli.py status --symbol BTCUSDT --order-id <id>`

## Advanced Usage

### Programmatic Access

```python
from trading_bot.bot import BinanceClient, OrderManager
from trading_bot.bot.validators import validate_order_params

# Initialize
client = BinanceClient()
manager = OrderManager(client)

try:
    # Validate input
    symbol, side, otype, qty, price = validate_order_params(
        "BTCUSDT", "BUY", "LIMIT", 0.01, 45000.00
    )
    
    # Place order
    response = manager.place_limit_order(symbol, side, qty, price)
    
    # Process response
    print(f"Order {response['orderId']} placed with status {response['status']}")

except Exception as e:
    print(f"Error: {e}")
```

### Custom Logging

```python
from trading_bot.bot.logging_config import setup_logger

logger = setup_logger(__name__)

logger.info("Starting trading bot")
logger.debug("Detailed debug information")
logger.error("An error occurred")
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| requests | 2.31.0 | HTTP requests to Binance API |
| python-dotenv | 1.0.0 | Load environment variables |
| click | 8.1.7 | Professional CLI interface |
| tabulate | 0.9.0 | Pretty table formatting |
| colorama | 0.4.6 | Colored terminal output |

## Assumptions & Limitations

### Assumptions
1. ✅ Testnet accounts and API credentials are pre-configured
2. ✅ Python 3.8+ is available
3. ✅ Network connectivity to testnet.binancefuture.com
4. ✅ Orders are for spot futures (USDT-M)

### Current Limitations
⚠️ This is a testnet-only trading bot
- Unable to place real orders on mainnet
- Testnet balances are for testing purposes
- Order types limited to MARKET and LIMIT

### Future Enhancements
- [ ] Bracket orders (Stop-Loss + Take-Profit)
- [ ] OCO orders (One-Cancels-Other)
- [ ] TWAP execution (Time-Weighted Average Price)
- [ ] Grid trading strategy
- [ ] GUI dashboard
- [ ] Order templates/presets
- [ ] Order history export

## Security Notes

⚠️ **Important**

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use testnet credentials only** - Never use mainnet keys
3. **Regenerate keys periodically** - For security best practice
4. **Use IP whitelist** - On Binance API key settings
5. **Disable withdraw permission** - Remove fund withdrawal permission

## Support & Issues

For issues or questions:

1. Check the **Troubleshooting** section above
2. Review log files in `logs/` directory
3. Verify API credentials and testnet URL
4. Compare against the examples in this README

## License

This project is provided as-is for testing and educational purposes.

## Disclaimer

⚠️ **Always test thoroughly on the testnet before using any real funds.** This bot is provided for educational and testing purposes. Use at your own risk.

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Tested on:** Python 3.8+
#   t r a d i n g - b o t  
 #   t r a d i n g - b o t  
 
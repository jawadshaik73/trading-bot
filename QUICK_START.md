# 🚀 Quick Start Guide - Trading Bot (Mock Mode)

## ✅ No API Keys Required!

This trading bot now works **completely offline** in **MOCK MODE** by default. No Binance API keys needed!

---

## 📦 Installation

```bash
# 1. Navigate to the project directory
cd trading-bot

# 2. Install dependencies
pip install -r requirements.txt
```

That's it! The bot is ready to use.

---

## 🎯 Quick Test

Test that everything is working:

```bash
python cli.py test
```

You should see:
```
============================================================
  🤖 Trading Bot - [MOCK MODE]
  v1.0.0 - Professional Trading Interface
============================================================

✓ MOCK EXCHANGE READY
Mode: MOCK (Offline)
Status: ✓ Working
API Calls: None (Completely Offline)
USDT Balance: $10000.00

✓ Mock exchange is ready for testing!
ℹ No API credentials needed in mock mode
```

---

## 💰 Place Your First Order

### Market Order (Buy Bitcoin)

```bash
python cli.py market --symbol BTCUSDT --side BUY --quantity 0.001
```

The bot will:
1. Show you an order summary
2. Ask for confirmation
3. Execute the order instantly (no real money!)
4. Display the order details

### Example Output:
```
Order Summary:
Symbol      BTC/USDT
Side        BUY
Type        MARKET
Quantity    0.001
Price       Market Price

Execute this order? [Y/n]: y

✓ ORDER PLACED SUCCESSFULLY
Order ID        1000
Symbol          BTC/USDT
Side            BUY
Status          CLOSED
Quantity        0.001
Executed Qty    0.001
Avg Price       45045.00
Quote Qty       45.05
```

---

## 🎮 Available Commands

### 1. Test Connection
```bash
python cli.py test
```

### 2. Place Market Order
```bash
python cli.py market
```
Interactive mode - will prompt for symbol, side, and quantity

Or with parameters:
```bash
python cli.py market --symbol ETHUSDT --side SELL --quantity 0.1
```

### 3. Get Help
```bash
python cli.py --help
```

---

## 🔧 Exchange Modes

The bot supports three modes (configured in `.env`):

### 1. **MOCK Mode** (Default - Recommended)
- ✅ Completely offline
- ✅ No API keys required
- ✅ Instant execution
- ✅ Perfect for testing
- ✅ $10,000 starting balance

```env
EXCHANGE_MODE=mock
```

### 2. **CCXT Mode** (For Real Trading)
- ⚠️ Requires Binance API keys
- ⚠️ Real money trading
- ⚠️ Use with caution

```env
EXCHANGE_MODE=ccxt
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
CCXT_SANDBOX_MODE=False
```

### 3. **Binance Mode** (Legacy)
- ⚠️ Requires Binance testnet API keys
- ⚠️ Uses legacy REST API

```env
EXCHANGE_MODE=binance
BINANCE_API_KEY=your_testnet_key
BINANCE_API_SECRET=your_testnet_secret
```

---

## 📊 Supported Trading Pairs (Mock Mode)

- **BTC/USDT** - Bitcoin
- **ETH/USDT** - Ethereum
- **BNB/USDT** - Binance Coin
- **ADA/USDT** - Cardano
- **SOL/USDT** - Solana

You can use either format:
- `BTCUSDT` (Binance format)
- `BTC/USDT` (CCXT format)

The bot automatically converts between formats.

---

## 🎓 Example Workflow

```bash
# 1. Test the bot
python cli.py test

# 2. Buy some Bitcoin
python cli.py market --symbol BTCUSDT --side BUY --quantity 0.01

# 3. Sell some Ethereum
python cli.py market --symbol ETHUSDT --side SELL --quantity 0.5

# 4. Check logs
cat logs/__main__.log
```

---

## 📝 Logs

All operations are logged to the `logs/` directory:

- `__main__.log` - CLI operations
- `trading_bot_bot_mock_exchange.log` - Mock exchange operations
- `trading_bot_bot_ccxt_client.log` - CCXT operations (if using CCXT mode)
- `trading_bot_bot_client.log` - Binance client operations (if using Binance mode)

---

## 🔄 Switching Modes

To switch from mock mode to real trading:

1. Edit `.env` file:
```env
EXCHANGE_MODE=ccxt  # Change from 'mock' to 'ccxt'
BINANCE_API_KEY=your_real_api_key
BINANCE_API_SECRET=your_real_api_secret
CCXT_SANDBOX_MODE=False  # Set to False for live trading
```

2. Test the connection:
```bash
python cli.py test
```

3. Start with small orders!

---

## ⚠️ Important Notes

### Mock Mode
- **No real money** - All trades are simulated
- **Offline** - No internet required
- **Instant** - No API delays
- **Safe** - Perfect for learning and testing

### Live Trading (CCXT/Binance Mode)
- **Real money** - Actual trades on Binance
- **Requires API keys** - Get from Binance
- **Rate limits** - Subject to exchange limits
- **Risk** - Start with small amounts!

---

## 🆘 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Command not found: python"
Try `python3` instead:
```bash
python3 cli.py test
```

### Want to reset mock balance?
Just restart the bot - mock exchange resets to $10,000 USDT each time.

---

## 🎉 Next Steps

1. ✅ Test the bot in mock mode
2. ✅ Try different trading pairs
3. ✅ Experiment with different quantities
4. ✅ Check the logs to see what's happening
5. ✅ When ready, switch to CCXT mode with testnet
6. ⚠️ Only use live mode after extensive testing!

---

## 📚 More Information

- Full documentation: `README.md`
- CCXT guide: `CCXT_SANDBOX_GUIDE.md`
- Example scripts: `examples_ccxt_sandbox.py`

---

**Happy Trading! 🚀**

*Remember: Always test thoroughly in mock mode before using real money!*

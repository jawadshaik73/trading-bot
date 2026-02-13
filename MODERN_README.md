# 🚀 Modern Trading Bot

A completely modernized trading bot with **multiple authentication options** and **no .env file requirements**!

## ✨ Modern Features

### 🔓 No More .env Files!
- **Interactive Authentication**: API keys prompted when needed
- **Environment Variables**: Still supported as fallback
- **Configuration Files**: Optional JSON config support
- **Mock Mode**: Default safe mode (no API keys required)

### 🎯 Multiple Exchange Modes
1. **Mock Mode** (Default) - Completely offline, perfect for testing
2. **CCXT Mode** - Industry-standard library with interactive auth
3. **Binance REST Mode** - Direct API with interactive auth

### 🛡️ Safety First
- Defaults to **mock mode** for safety
- **No accidental live trading**
- Clear mode indicators and warnings
- Interactive confirmation for all orders

## 🚀 Quick Start (No Setup Required!)

### 1. Run Immediately (Mock Mode)
```bash
# No setup needed! Just run:
python main.py info
```

The bot will start in **mock mode** - completely offline with simulated trading.

### 2. Try Trading (Mock Mode)
```bash
python main.py market
# Follow the prompts to place a mock trade
```

### 3. Check Balance (Mock Mode)
```bash
python main.py balance
# View simulated account balance
```

## 🔧 Real Trading Setup

### Option 1: Interactive Authentication (Recommended)
```bash
# Set exchange mode to CCXT or binance
export EXCHANGE_MODE=ccxt  # or "binance"

# Run any command - you'll be prompted for API keys
python main.py market
```

When you run a command, you'll be prompted for your API keys:
```
Enter Binance API Key: your_api_key_here
Enter Binance API Secret: your_api_secret_here
```

### Option 2: Environment Variables (Traditional)
```bash
# Set environment variables
export EXCHANGE_MODE=ccxt
export BINANCE_API_KEY=your_api_key_here
export BINANCE_API_SECRET=your_api_secret_here

# Run commands without prompts
python main.py market
```

### Option 3: Configuration File
```bash
# Create trading_bot_config.json
{
  "exchange_mode": "ccxt",
  "api_key": "your_api_key_here",
  "api_secret": "your_api_secret_here"
}

# Run commands - config will be auto-detected
python main.py market
```

## 🎮 Available Commands

### Market Order
```bash
python main.py market
# Interactive order placement
```

### Account Balance
```bash
python main.py balance
# View account balance and positions
```

### API Test
```bash
python main.py test
# Test API connection and authentication
```

### Configuration Info
```bash
python main.py info
# Show current configuration and mode
```

## ⚙️ Configuration Options

### Exchange Modes
- `mock` - Offline testing (default)
- `ccxt` - CCXT library (recommended for real trading)
- `binance` - Binance REST API (legacy)

### Environment Variables
```bash
export EXCHANGE_MODE=mock|ccxt|binance
export BINANCE_API_KEY=your_key
export BINANCE_API_SECRET=your_secret
export CCXT_SANDBOX_MODE=true|false
```

### Configuration File
Create `trading_bot_config.json`:
```json
{
  "exchange_mode": "ccxt",
  "api_key": "your_api_key",
  "api_secret": "your_api_secret",
  "sandbox_mode": true,
  "log_level": "INFO"
}
```

## 🛡️ Safety Features

### Default Safe Mode
- **Mock mode by default** - No accidental real trading
- **Interactive prompts** - Confirm every order
- **Clear warnings** - Know when you're in live mode

### Mode Indicators
```
🤖 Modern Trading Bot - [MOCK MODE]
🤖 Modern Trading Bot - [CCXT MODE]
🤖 Modern Trading Bot - [BINANCE MODE]
```

### Color-Coded Output
- 🟢 **Green**: Mock mode (safe)
- 🟡 **Yellow**: Live mode (be careful!)
- 🔴 **Red**: Errors and warnings

## 🔄 Migration from Legacy

### Before (Old Way)
```bash
# Required .env file
# Manual setup needed
# Risk of accidental live trading
```

### After (Modern Way)
```bash
# No setup required
# Runs in mock mode by default
# Safe and interactive
```

### Update Your Workflow
1. Delete your `.env` file (optional)
2. Run `python main.py` instead of `python cli.py`
3. Enjoy interactive authentication!

## 🚨 Important Notes

### Binance Testnet
- Get testnet API keys from: https://testnet.binancefuture.com
- **Never use real money on testnet!**
- Testnet has separate registration from mainnet

### Live Trading Warning
```bash
# WARNING: These will trade with real money!
export EXCHANGE_MODE=ccxt
export CCXT_SANDBOX_MODE=false
```

### Best Practices
1. Always test in **mock mode** first
2. Use **testnet** before live trading
3. Keep API keys secure
4. Monitor your orders carefully

## 🛠️ Technical Details

### File Structure
```
trading-bot/
├── main.py              # Modern entry point
├── cli_modern.py        # Modern CLI with interactive auth
├── config_modern.py     # Modern configuration system
├── trading_bot_config.example.json  # Config template
├── MODERN_README.md     # This file
└── (legacy files remain unchanged)
```

### Backward Compatibility
- All legacy functionality preserved
- `.env` files still supported
- Old `cli.py` still works
- No breaking changes

## 🆘 Getting Help

### Common Issues
1. **"No module named 'click'"** - Run `pip install -r requirements.txt`
2. **API connection errors** - Check your API keys and internet connection
3. **Order failures** - Check symbol format and trading permissions

### Support
- Check exchange status: https://status.binance.com/
- Testnet support: https://testnet.binancefuture.com
- API documentation: https://binance-docs.github.io/apidocs/

---

**Happy Trading! 🚀**

*Remember: Always test in mock mode first, and never trade more than you can afford to lose.*
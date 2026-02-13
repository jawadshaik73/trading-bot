"""
Configuration module for Binance API credentials and trading settings.
Supports both traditional REST API and CCXT library with sandbox mode.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# EXCHANGE MODE CONFIGURATION
# ============================================================================
# Determines which exchange client to use
# Options: "mock", "binance"
# - mock: MockExchange (completely offline, no API calls, perfect for testing)
# - binance: BinanceClient (Binance Futures Testnet REST API, requires API keys)
EXCHANGE_MODE = os.getenv("EXCHANGE_MODE", "mock").lower()

# ============================================================================
# LEGACY API CONFIGURATION (Traditional REST API)
# ============================================================================
BINANCE_TESTNET_BASE_URL = "https://testnet.binancefuture.com"
API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# ============================================================================
# BINANCE API CONFIGURATION (Only used when EXCHANGE_MODE=binance)
# ============================================================================
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_DIR = "logs"
LOG_LEVEL = "INFO"

# ============================================================================
# TRADING LIMITS (Safety guardrails)
# ============================================================================
MAX_ORDER_QUANTITY = 1000
MIN_ORDER_QUANTITY = 0.001

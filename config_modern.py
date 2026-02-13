"""
Modern configuration module with multiple authentication options.
Supports interactive input, environment variables, and config files.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load .env file for environment variables
load_dotenv()
from dotenv import load_dotenv

# Load .env file for environment variables
load_dotenv()

# ============================================================================
# EXCHANGE MODE CONFIGURATION
# ============================================================================
# Default to mock mode for safe testing
def get_exchange_mode() -> str:
    """Get exchange mode with multiple fallback options."""
    # 1. Check environment variable
    mode = os.getenv("EXCHANGE_MODE")
    if mode and mode.lower() in ["mock", "ccxt", "binance"]:
        return mode.lower()
    
    # 2. Check for API keys in environment
    if os.getenv("BINANCE_API_KEY") and os.getenv("BINANCE_API_SECRET"):
        return "ccxt"
    
    # 3. Check config file
    config_file = Path("trading_bot_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                if "exchange_mode" in config and config["exchange_mode"] in ["mock", "ccxt", "binance"]:
                    return config["exchange_mode"]
        except (json.JSONDecodeError, KeyError):
            pass
    
    # 4. Default to mock mode (safest option)
    return "mock"

EXCHANGE_MODE = get_exchange_mode()

# ============================================================================
# API CREDENTIALS CONFIGURATION
# ============================================================================
class APIConfig:
    """API configuration with multiple authentication methods."""
    
    def __init__(self):
        self.api_key = ""
        self.api_secret = ""
        self._load_credentials()
    
    def _load_credentials(self) -> None:
        """Load API credentials from multiple sources with priority:
        1. Environment variables
        2. Config file
        3. Interactive input (if needed)
        """
        # Try environment variables first
        self.api_key = os.getenv("BINANCE_API_KEY", "")
        self.api_secret = os.getenv("BINANCE_API_SECRET", "")
        
        if self.api_key and self.api_secret:
            return
        
        # Try config file
        config_file = Path("trading_bot_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get("api_key", "")
                    self.api_secret = config.get("api_secret", "")
                    if self.api_key and self.api_secret:
                        return
            except (json.JSONDecodeError, KeyError):
                pass
        
        # For mock mode, credentials aren't needed
        if EXCHANGE_MODE == "mock":
            return
            
        # For real modes, we can prompt interactively if running in CLI context
        # This will be handled by the CLI when needed
    
    def get_credentials(self) -> tuple[str, str]:
        """Get API credentials, prompting interactively if missing and in CLI context."""
        return self.api_key, self.api_secret
    
    def prompt_for_credentials(self) -> None:
        """Prompt user for API credentials interactively."""
        if not self.api_key:
            self.api_key = input("Enter Binance API Key: ").strip()
        if not self.api_secret:
            self.api_secret = input("Enter Binance API Secret: ").strip()

# Global API configuration instance
API_CONFIG = APIConfig()

# ============================================================================
# BINANCE API CONFIGURATION
# ============================================================================
BINANCE_TESTNET_BASE_URL = "https://testnet.binancefuture.com"
BINANCE_LIVE_BASE_URL = "https://fapi.binance.com"

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

# ============================================================================
# SANDBOX MODE CONFIGURATION
# ============================================================================
def get_sandbox_mode() -> bool:
    """Get sandbox mode setting."""
    # Note: Binance removed futures sandbox, but we keep this for CCXT compatibility
    sandbox = os.getenv("CCXT_SANDBOX_MODE", "").lower()
    if sandbox in ["true", "1", "yes"]:
        return True
    elif sandbox in ["false", "0", "no"]:
        return False
    
    # Default to True for safety
    return True

CCXT_SANDBOX_MODE = get_sandbox_mode()
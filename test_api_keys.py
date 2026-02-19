#!/usr/bin/env python3
"""
Test script to verify if Binance API keys are working properly.
"""
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ccxt_api():
    """Test API keys using CCXT library with sandbox support."""
    try:
        import ccxt
        
        api_key = os.getenv("BINANCE_API_KEY", "")
        api_secret = os.getenv("BINANCE_API_SECRET", "")
        sandbox_mode = os.getenv("CCXT_SANDBOX_MODE", "True").lower() in ("true", "1", "yes")
        
        print(f"Testing Binance API Keys with CCXT (Sandbox: {sandbox_mode})...")
        print("=" * 60)
        print(f"API Key (first 10 chars): {api_key[:10]}...")
        print(f"API Secret (first 10 chars): {api_secret[:10]}...")
        print("=" * 60)
        
        if not api_key or not api_secret:
            print("ERROR: API keys are not set in .env file!")
            return False
        
        # Initialize CCXT Binance exchange
        exchange_config = {
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
            }
        }
        
        exchange = ccxt.binance(exchange_config)
        
        if sandbox_mode:
            print("Enabling Sandbox Mode (Testnet)...")
            exchange.set_sandbox_mode(True)
        else:
            print("Using LIVE Mode (Mainnet)...")
        
        # Test 1: Fetch balance
        print("\nTest 1: Fetching account balance...")
        try:
            balance = exchange.fetch_balance()
            print("SUCCESS: API keys are WORKING!")
            print(f"\nAccount Balance Type: {exchange.options.get('defaultType', 'N/A')}")
            
            # Display USDT balance and total
            if 'USDT' in balance:
                usdt = balance['USDT']
                print(f"   USDT Free: {usdt.get('free', 0)}")
                print(f"   USDT Used: {usdt.get('used', 0)}")
                print(f"   USDT Total: {usdt.get('total', 0)}")
            else:
                print("   No USDT balance found (account might be empty or wrong type)")
            
            print("\nAPI Connection: VALID AND WORKING")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"FAILED: {error_msg}")

            # More detailed handling for the common Binance -2015 error
            if "-2015" in error_msg or "Invalid API-key" in error_msg or "permissions" in error_msg.lower():
                print("\nIssue: Invalid API-key, IP, or permissions for action (Binance -2015)")
                print("   Likely causes and fixes:")
                print("   1) IP restriction: Add your public IP to the key's IP whitelist.")
                print("   2) Mainnet vs Testnet mismatch: Ensure you're using Testnet keys when sandbox mode is ON.")
                print(f"      Current Sandbox setting: {'ON' if sandbox_mode else 'OFF'}")
                print("   3) Missing permissions: Enable 'Futures' in API settings.")
                try:
                    public_ip = requests.get('https://api.ipify.org', timeout=3).text
                    print(f"   Your public IP (detected): {public_ip}")
                except Exception:
                    print("   Your public IP: Unable to detect automatically")
                print("\n   Quick actions:")
                print("     - Open Binance API Management and edit the key 'jawad123'")
                print("     - Add your public IP or use Testnet keys for testing")
                print("     - If you're unsure, run: python SETUP_API_KEY.py for a complete guide")

            elif "401" in error_msg or "unauthorized" in error_msg.lower():
                print("\nIssue: Invalid API Key or Secret (Unauthorized)")
            elif "403" in error_msg or "forbidden" in error_msg.lower():
                print("\nIssue: Forbidden (Check permissions)")

            return False
    
    except ImportError:
        print("ERROR: CCXT library not installed")
        return False

def test_binance_rest_api():
    """Test API keys using Binance REST API with dynamic URL."""
    try:
        import requests
        import hmac
        import hashlib
        import time
        
        api_key = os.getenv("BINANCE_API_KEY", "")
        api_secret = os.getenv("BINANCE_API_SECRET", "")
        sandbox_mode = os.getenv("CCXT_SANDBOX_MODE", "True").lower() in ("true", "1", "yes")
        
        # Choose base URL based on sandbox mode
        if sandbox_mode:
            base_url = "https://testnet.binancefuture.com"
            print(f"\nTest 2: Using Binance REST API (TESTNET)...")
        else:
            base_url = "https://fapi.binance.com"
            print(f"\nTest 2: Using Binance REST API (MAINNET)...")
            
        print("=" * 60)
        
        timestamp = int(time.time() * 1000)
        params = f"timestamp={timestamp}"
        
        signature = hmac.new(
            api_secret.encode(),
            params.encode(),
            hashlib.sha256
        ).hexdigest()
        
        url = f"{base_url}/fapi/v2/account"
        headers = {"X-MBX-APIKEY": api_key}
        
        try:
            response = requests.get(
                url,
                params={'timestamp': timestamp, 'signature': signature},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("SUCCESS: REST API authentication WORKING!")
                data = response.json()
                print(f"\nAccount Details:")
                print(f"   Can Trade: {data.get('canTrade', 'N/A')}")
                print(f"   Account Type: {data.get('accountType', 'N/A')}")
                return True
            else:
                print(f"FAILED: Status Code {response.status_code}")
                print(f"   Response: {response.text}")
                if "-2015" in response.text:
                    print("   Hint: Check 'Enable Futures' in API settings or match Mainnet/Testnet keys.")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")
            return False
            
    except Exception as e:
        print(f"REST API Test Error: {e}")
        return False

if __name__ == "__main__":
    import requests # Ensure requests is available for IP check
    print("\n" + "=" * 60)
    print("TRADING BOT - API KEY VALIDATION TEST")
    print("=" * 60 + "\n")
    
    # Check current exchange mode
    exchange_mode = os.getenv("EXCHANGE_MODE", "mock").lower()
    sandbox_mode = os.getenv("CCXT_SANDBOX_MODE", "True").lower() in ("true", "1", "yes")
    
    print(f"Current EXCHANGE_MODE: {exchange_mode}")
    print(f"Current SANDBOX_MODE: {sandbox_mode}")
    
    if exchange_mode == "mock":
        print("WARNING: Running in MOCK mode (API keys not used locally)")
        print("   API keys will be tested, but the bot is using MockExchange")
        print("\n")
    
    # Run tests
    ccxt_result = test_ccxt_api()
    rest_result = test_binance_rest_api()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if ccxt_result or rest_result:
        print("API Keys are VALID and WORKING")
        if not ccxt_result: print("   (REST API passed, but CCXT failed - check CCXT version/config)")
        if not rest_result: print("   (CCXT passed, but REST API failed - check network/URL)")
        
        print("\nTo use real API instead of mock mode:")
        print("   1. Edit .env file")
        print("   2. Change: EXCHANGE_MODE=ccxt")
        print("   3. Run: python cli.py info")
    else:
        print("API Keys are NOT WORKING - Likely Causes:")
        print("   1. 'Enable Futures' is NOT checked in Binance API settings (Common!)")
        print("   2. Using Mainnet keys with CCXT_SANDBOX_MODE=True (or vice versa)")
        print("   3. IP address is not whitelisted (if restricted)")
    
    print("=" * 60 + "\n")
    
    sys.exit(0 if ccxt_result or rest_result else 1)


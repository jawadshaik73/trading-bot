#!/usr/bin/env python3
"""
Advanced Diagnostic Tool - API Key Validation & Troubleshooting
Detects your public IP and provides actionable fixes
"""
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

def get_public_ip():
    """Detect public IP address"""
    try:
        import socket
        import urllib.request
        ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf-8')
        return ip
    except:
        return None

def check_env_credentials():
    """Verify credentials are loaded from .env"""
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    sandbox = os.getenv("CCXT_SANDBOX_MODE", "False").lower() in ("true", "1", "yes")
    exchange_mode = os.getenv("EXCHANGE_MODE", "mock").lower()
    
    print("\n" + "=" * 70)
    print("🔍 CONFIGURATION CHECK")
    print("=" * 70)
    print(f"EXCHANGE_MODE:          {exchange_mode}")
    print(f"CCXT_SANDBOX_MODE:      {sandbox}")
    print(f"API Key loaded:         {'✅ YES' if api_key else '❌ NO'} ({len(api_key)} chars)")
    print(f"API Secret loaded:      {'✅ YES' if api_secret else '❌ NO'} ({len(api_secret)} chars)")
    
    if api_key:
        print(f"API Key (first 15):     {api_key[:15]}...")
        print(f"API Key (last 10):      ...{api_key[-10:]}")
    
    if not api_key or not api_secret:
        print("\n❌ ERROR: Credentials not loaded!")
        return False
    
    return True, api_key, api_secret, sandbox

def test_api_with_requests():
    """Test API key using raw requests"""
    try:
        import requests
        import hmac
        import hashlib
        import time
        
        api_key = os.getenv("BINANCE_API_KEY", "").strip()
        api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
        sandbox = os.getenv("CCXT_SANDBOX_MODE", "False").lower() in ("true", "1", "yes")
        
        # Determine endpoint
        if sandbox:
            base_url = "https://testnet.binancefuture.com"
            print("\n📍 Testing TESTNET (Sandbox Mode ON)")
        else:
            base_url = "https://fapi.binance.com"
            print("\n📍 Testing MAINNET (Sandbox Mode OFF)")
        
        print("=" * 70)
        
        # Create timestamp and signature
        timestamp = int(time.time() * 1000)
        query_string = f"timestamp={timestamp}"
        
        signature = hmac.new(
            api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'X-MBX-APIKEY': api_key,
            'Content-Type': 'application/json'
        }
        
        url = f"{base_url}/fapi/v2/account"
        
        print(f"Endpoint:               {url}")
        print("Sending request...")
        
        response = requests.get(
            url,
            params={'timestamp': timestamp, 'signature': signature},
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code:            {response.status_code}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! API Key is VALID and WORKING!")
            data = response.json()
            print(f"✅ Account Type:        {data.get('accountType', 'N/A')}")
            print(f"✅ Can Trade:           {data.get('canTrade', 'N/A')}")
            return True
        else:
            print(f"\n❌ FAILED with Status {response.status_code}")
            try:
                error = response.json()
                error_code = error.get('code', 'Unknown')
                error_msg = error.get('msg', 'Unknown error')
                print(f"Error Code:             {error_code}")
                print(f"Error Message:          {error_msg}")
                return False, error_code, error_msg
            except:
                print(f"Response:               {response.text}")
                return False, None, response.text
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, None, str(e)

def show_solution(error_code=None):
    """Show detailed solution based on error"""
    public_ip = get_public_ip()
    
    print("\n" + "=" * 70)
    print("💡 SOLUTION GUIDE")
    print("=" * 70)
    
    if error_code == "-2015":
        print("\nError -2015: Invalid API-key, IP, or permissions")
        print("\nPossible causes:")
        print("1. IP Restriction Issue")
        print(f"   Your public IP: {public_ip if public_ip else 'Unable to detect'}")
        if public_ip:
            print(f"   → Add this IP to Binance API whitelist: {public_ip}/32")
        else:
            print(f"   → Visit https://www.ipchicken.com/ to find your IP")
        print("   → Or leave whitelist EMPTY to allow all IPs (less secure)")
        
        print("\n2. Sandbox/Mainnet Mismatch")
        sandbox = os.getenv("CCXT_SANDBOX_MODE", "False").lower() in ("true", "1", "yes")
        print(f"   Current mode: {'TESTNET (Sandbox)' if sandbox else 'MAINNET (Live)'}")
        print("   → If using Testnet keys, set CCXT_SANDBOX_MODE=True")
        print("   → If using Mainnet keys, set CCXT_SANDBOX_MODE=False")
        
        print("\n3. Missing Permissions")
        print("   → Enable 'Futures Trading' or 'Spot & Margin Trading' in API settings")
        print("   → Make sure key is NOT restricted to reading only")
        
    print("\n" + "=" * 70)
    print("🚀 RECOMMENDED ACTIONS (Choose ONE):")
    print("=" * 70)
    
    print("\n✅ OPTION 1: Use MOCK Mode (Safest for testing)")
    print("   → Requires NO API keys, works completely offline")
    print("   → Edit .env: EXCHANGE_MODE=mock")
    print("   → Run: python main.py test")
    
    print("\n✅ OPTION 2: Fix current API key")
    print("   Step 1: Go to Binance API Management")
    print(f"   Step 2: Add IP {public_ip if public_ip else 'YOUR_IP'}/32 to whitelist")
    print("   Step 3: Wait 5 minutes")
    print("   Step 4: Run: python test_api_keys_advanced.py")
    
    print("\n✅ OPTION 3: Generate new Testnet key")
    print("   Step 1: Go to https://testnet.binancefuture.com")
    print("   Step 2: Create new API key")
    print("   Step 3: Update .env with new key/secret")
    print("   Step 4: Set CCXT_SANDBOX_MODE=True")
    print("   Step 5: Run: python test_api_keys_advanced.py")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🤖 ADVANCED API DIAGNOSTICS")
    print("=" * 70)
    
    # Check environment
    result = check_env_credentials()
    
    if not result:
        print("\n❌ Cannot proceed - credentials missing from .env")
        sys.exit(1)
    
    is_valid, api_key, api_secret, sandbox = result
    
    # Test API
    test_result = test_api_with_requests()
    
    if isinstance(test_result, tuple):
        success, error_code, error_msg = test_result
        if not success:
            show_solution(error_code)
    else:
        if test_result:
            print("\n✅ Your API key is working correctly!")
            print("\nNext steps:")
            print("  1. Set EXCHANGE_MODE=ccxt in .env")
            print("  2. Run: python main.py market")
    
    print("\n" + "=" * 70)

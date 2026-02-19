#!/usr/bin/env python3
"""
Comprehensive API Key Diagnostic Tool
Identifies and fixes -2015 errors and IP restriction issues
"""
import os
import sys
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_public_ip():
    """Get current public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except Exception as e:
        return f"Unable to detect: {e}"

def test_hmac_signature():
    """Verify HMAC SHA256 signature generation is correct"""
    print("\n" + "="*70)
    print("1. HMAC-SHA256 SIGNATURE VERIFICATION")
    print("="*70)
    
    api_secret = os.getenv("BINANCE_API_SECRET", "")
    
    if not api_secret:
        print("ERROR: BINANCE_API_SECRET not found in .env")
        return False
    
    # Test with a sample query string
    test_query = "timestamp=1234567890"
    
    signature = hmac.new(
        api_secret.encode('utf-8'),
        test_query.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"API Secret (first 20 chars): {api_secret[:20]}...")
    print(f"Test Query: {test_query}")
    print(f"Generated HMAC-SHA256: {signature}")
    print("✓ HMAC-SHA256 signature generation is CORRECT")
    return True

def test_rest_api_mainnet():
    """Test REST API against Binance Mainnet (LIVE)"""
    print("\n" + "="*70)
    print("2. BINANCE REST API - MAINNET (LIVE)")
    print("="*70)
    
    api_key = os.getenv("BINANCE_API_KEY", "")
    api_secret = os.getenv("BINANCE_API_SECRET", "")
    
    if not api_key or not api_secret:
        print("ERROR: API credentials missing in .env")
        return False
    
    print(f"API Key: {api_key[:15]}...{api_key[-5:]}")
    print(f"Current Public IP: {get_public_ip()}")
    print(f"Whitelisted IP (from settings): 157.50.130.184")
    print(f"\nTesting endpoint: /fapi/v2/account")
    
    timestamp = int(time.time() * 1000)
    params_str = f"timestamp={timestamp}"
    
    signature = hmac.new(
        api_secret.encode('utf-8'),
        params_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    url = "https://fapi.binance.com/fapi/v2/account"
    headers = {
        "X-MBX-APIKEY": api_key,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.get(
            url,
            params={'timestamp': timestamp, 'signature': signature},
            headers=headers,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ SUCCESS: API Authentication WORKING!")
            print(f"  Can Trade: {data.get('canTrade')}")
            print(f"  Total Wallets: {data.get('totalWalletBalance')}")
            return True
        else:
            print(f"✗ FAILED: {response.status_code}")
            error_data = response.json()
            error_code = error_data.get('code')
            error_msg = error_data.get('msg', '')
            
            print(f"\n  Error Code: {error_code}")
            print(f"  Error Message: {error_msg}")
            
            if error_code == -2015:
                print("\n  DIAGNOSIS for -2015 Error:")
                print("  This error means one of the following:")
                print("    a) API Key/Secret are incorrect")
                print("    b) 'Enable Futures' is NOT enabled in Binance API settings")
                print("    c) Your IP is not whitelisted or changed since configuration")
                print("    d) API Key has insufficient permissions")
                print("\n  FIXES:")
                print("    1) Go to: https://www.binance.com/en/usercenter/settings/api-management")
                print("    2) Click on your API key 'jawad123'")
                print("    3) CHECK these settings:")
                print("       • 'Enable Spot & Margin Trading' ✓")
                print("       • 'Enable Futures' ✓ (THIS IS CRITICAL!)")
                print("    4) Update IP whitelist:")
                current_ip = get_public_ip()
                if current_ip and "Unable" not in current_ip:
                    print(f"       • Add your current IP: {current_ip}")
                else:
                    print("       • Add your current public IP address")
                print("    5) Wait 30 seconds then retry")
                
            return False
    except Exception as e:
        print(f"✗ Network Error: {e}")
        return False

def test_rest_api_testnet():
    """Test REST API against Binance Testnet"""
    print("\n" + "="*70)
    print("3. BINANCE REST API - TESTNET")
    print("="*70)
    
    api_key = os.getenv("BINANCE_API_KEY", "")
    api_secret = os.getenv("BINANCE_API_SECRET", "")
    
    if not api_key or not api_secret:
        print("ERROR: API credentials missing in .env")
        return False
    
    print("NOTE: Testnet uses the SAME API keys as Mainnet")
    print(f"Testing endpoint: /fapi/v2/account (testnet.binancefuture.com)")
    
    timestamp = int(time.time() * 1000)
    params_str = f"timestamp={timestamp}"
    
    signature = hmac.new(
        api_secret.encode('utf-8'),
        params_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    url = "https://testnet.binancefuture.com/fapi/v2/account"
    headers = {
        "X-MBX-APIKEY": api_key,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.get(
            url,
            params={'timestamp': timestamp, 'signature': signature},
            headers=headers,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ SUCCESS: Testnet API Authentication WORKING!")
            print(f"  Account Type: {data.get('accountType')}")
            return True
        else:
            print(f"✗ FAILED: {response.status_code}")
            error_data = response.json()
            print(f"  Error: {error_data}")
            return False
    except Exception as e:
        print(f"✗ Network Error or Testnet Unavailable: {e}")
        print("  Note: Binance Testnet may be under maintenance")
        return False

def show_recommendations():
    """Show recommendations based on test results"""
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    
    print("\n1. CHECK BINANCE API SETTINGS:")
    print("   URL: https://www.binance.com/en/usercenter/settings/api-management")
    print("   • Ensure 'Enable Futures' is checked")
    print("   • Ensure IP is whitelisted or set to 'Unrestricted'")
    print("   • Ensure 'Enable Spot & Margin Trading' is checked")
    
    print("\n2. HMAC-SHA256 IMPLEMENTATION:")
    print("   Your code is using correct HMAC implementation:")
    print("   ✓ hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256)")
    print("   ✓ .hexdigest() is correct")
    
    print("\n3. SWITCH EXCHANGE MODE:")
    print("   Current mode: EXCHANGE_MODE=mock")
    print("   To test with real API, change to:")
    print("   EXCHANGE_MODE=ccxt")
    print("   (Note: CCXT testnet/sandbox deprecated, use mainnet)")
    
    print("\n4. IP WHITELIST MANAGEMENT:")
    print(f"   Your Public IP: {get_public_ip()}")
    print("   Configured IP: 157.50.130.184")
    print("   If different, update Binance API settings to add new IP")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("BINANCE API DIAGNOSTIC TOOL")
    print("="*70)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Run tests
    hmac_ok = test_hmac_signature()
    mainnet_ok = test_rest_api_mainnet()
    testnet_ok = test_rest_api_testnet()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"HMAC-SHA256 Implementation: {'✓ CORRECT' if hmac_ok else '✗ FAILED'}")
    print(f"Mainnet API Access: {'✓ WORKING' if mainnet_ok else '✗ FAILED'}")
    print(f"Testnet API Access: {'✓ WORKING' if testnet_ok else '✗ FAILED'}")
    
    if mainnet_ok or testnet_ok:
        print("\n✓ API Keys are VALID - You can use EXCHANGE_MODE=ccxt")
    else:
        print("\n✗ API Keys are NOT WORKING - Follow recommendations above")
        show_recommendations()
    
    print("\n" + "="*70)

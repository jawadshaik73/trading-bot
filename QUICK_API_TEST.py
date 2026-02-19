#!/usr/bin/env python3
"""
Quick Test Script - Run after updating Binance API Settings
This is a fast, focused test to verify if your fixes worked
"""
import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

def quick_api_test():
    """Quick API test with minimal output"""
    
    api_key = os.getenv("BINANCE_API_KEY", "")
    api_secret = os.getenv("BINANCE_API_SECRET", "")
    
    print("\n🔍 QUICK API TEST")
    print("=" * 60)
    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    print(f"Testing: Binance Futures Mainnet")
    
    timestamp = int(time.time() * 1000)
    params_str = f"timestamp={timestamp}"
    
    signature = hmac.new(
        api_secret.encode('utf-8'),
        params_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    try:
        response = requests.get(
            "https://fapi.binance.com/fapi/v2/account",
            params={'timestamp': timestamp, 'signature': signature},
            headers={"X-MBX-APIKEY": api_key},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS! API is working!")
            print(f"   Can Trade: {data.get('canTrade')}")
            print(f"   Total Wallet Balance: {data.get('totalWalletBalance')} USDT")
            return True
        else:
            error = response.json()
            print(f"\n❌ FAILED (Status: {response.status_code})")
            print(f"   Error: {error.get('msg', 'Unknown error')}")
            print(f"\n💡 Next steps:")
            print(f"   1. Go to https://www.binance.com/en/usercenter/settings/api-management")
            print(f"   2. Enable 'Enable Futures' ✓")
            print(f"   3. Update IP to: 106.215.168.255")
            print(f"   4. Wait 30 seconds and retry")
            return False
            
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    success = quick_api_test()
    print("=" * 60 + "\n")
    exit(0 if success else 1)

#!/usr/bin/env python3
"""
HMAC-SHA256 Signature Guide & Verification
Shows exactly how Binance API signing works with your credentials
"""
import os
import time
import hmac
import hashlib
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

def demo_hmac_signing():
    """Demonstrate HMAC-SHA256 signing step by step"""
    
    api_secret = os.getenv("BINANCE_API_SECRET", "Ds4DgM0FRCvWtBfQY4te1ixCCQGWiEzhrj0Zf7ChJfrmLfJsNk5IeFuZ6B1AYWdP")
    
    print("\n" + "="*80)
    print("HMAC-SHA256 SIGNATURE GENERATION - COMPLETE WALKTHROUGH")
    print("="*80)
    
    # Step 1: Create query string
    print("\n📋 STEP 1: Create Query String")
    print("-" * 80)
    
    timestamp = int(time.time() * 1000)
    symbol = "BTCUSDT"
    side = "BUY"
    quantity = 0.001
    
    # Method 1: Simple timestamp-only request
    query_params_1 = {
        'timestamp': timestamp
    }
    
    query_string_1 = '&'.join([f"{k}={v}" for k, v in sorted(query_params_1.items())])
    print(f"\n  Query String (for /account endpoint):")
    print(f"  {query_string_1}")
    
    # Method 2: Order placement request
    query_params_2 = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
        'timestamp': timestamp
    }
    
    # Sort by key (IMPORTANT!)
    query_string_2 = '&'.join([f"{k}={v}" for k, v in sorted(query_params_2.items())])
    print(f"\n  Query String (for order placement):")
    print(f"  {query_string_2}")
    
    # Step 2: Generate HMAC
    print("\n\n🔐 STEP 2: Generate HMAC-SHA256")
    print("-" * 80)
    
    print(f"\n  API Secret: {api_secret[:20]}...{api_secret[-10:]}")
    print(f"  \n  Using Python hmac module:")
    print(f"    api_secret.encode('utf-8')")
    print(f"    query_string.encode('utf-8')")
    print(f"    hashlib.sha256")
    
    signature_1 = hmac.new(
        api_secret.encode('utf-8'),
        query_string_1.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    signature_2 = hmac.new(
        api_secret.encode('utf-8'),
        query_string_2.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"\n  Generated Signature (account query):")
    print(f"  {signature_1}")
    
    print(f"\n  Generated Signature (order placement):")
    print(f"  {signature_2}")
    
    # Step 3: Add signature to query string
    print("\n\n📍 STEP 3: Append Signature to Query String")
    print("-" * 80)
    
    final_url_1 = f"{query_string_1}&signature={signature_1}"
    final_url_2 = f"{query_string_2}&signature={signature_2}"
    
    print(f"\n  Final URL Parameter String (account):")
    print(f"  {final_url_1}")
    
    print(f"\n  Final URL Parameter String (order):")
    print(f"  {final_url_2}")

def compare_implementations():
    """Compare different HMAC generation approaches"""
    
    api_secret = os.getenv("BINANCE_API_SECRET", "Ds4DgM0FRCvWtBfQY4te1ixCCQGWiEzhrj0Zf7ChJfrmLfJsNk5IeFuZ6B1AYWdP")
    query_string = "timestamp=1234567890&symbol=BTCUSDT"
    
    print("\n\n" + "="*80)
    print("CORRECT vs INCORRECT IMPLEMENTATIONS")
    print("="*80)
    
    # ✓ CORRECT
    print("\n✅ CORRECT IMPLEMENTATION:")
    print("-" * 80)
    print("""
import hmac
import hashlib

signature = hmac.new(
    api_secret.encode('utf-8'),
    query_string.encode('utf-8'),
    hashlib.sha256
).hexdigest()
    """)
    
    correct_sig = hmac.new(
        api_secret.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"Result: {correct_sig}\n")
    
    # ❌ WRONG - No .hexdigest()
    print("❌ WRONG #1 - Missing .hexdigest():")
    print("-" * 80)
    print("""
signature = hmac.new(
    api_secret.encode('utf-8'),
    query_string.encode('utf-8'),
    hashlib.sha256
)  # Missing .hexdigest()!
    """)
    print("Result: <HMAC object> - NOT a string!\n")
    
    # ❌ WRONG - Not encoding strings
    print("❌ WRONG #2 - Not encoding strings:")
    print("-" * 80)
    print("""
signature = hmac.new(
    api_secret,  # Should be: api_secret.encode('utf-8')
    query_string,  # Should be: query_string.encode('utf-8')
    hashlib.sha256
).hexdigest()
    """)
    print("Result: TypeError - bytes expected\n")
    
    # ❌ WRONG - Wrong hash algorithm
    print("❌ WRONG #3 - Wrong hash algorithm:")
    print("-" * 80)
    print("""
signature = hmac.new(
    api_secret.encode('utf-8'),
    query_string.encode('utf-8'),
    hashlib.md5  # Wrong! Must be SHA256
).hexdigest()
    """)
    
    wrong_sig = hmac.new(
        api_secret.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.md5
    ).hexdigest()
    
    print(f"Result: {wrong_sig} - (Different from correct!)\n")

def test_real_signature():
    """Test with actual API secret"""
    
    api_secret = os.getenv("BINANCE_API_SECRET", "")
    if not api_secret:
        print("\nℹ️  No API secret found in .env")
        return
    
    print("\n" + "="*80)
    print("TEST WITH YOUR ACTUAL API CREDENTIALS")
    print("="*80)
    
    test_cases = [
        ("Account Query", "timestamp=1234567890"),
        ("With Symbol", "symbol=BTCUSDT&timestamp=1234567890"),
        ("Multiple Params", "quantity=0.001&side=BUY&symbol=BTCUSDT&timestamp=1234567890"),
    ]
    
    print(f"\nAPI Secret (first 20 chars): {api_secret[:20]}...")
    print("\nSignature Results:")
    print("-" * 80)
    
    for test_name, query_string in test_cases:
        signature = hmac.new(
            api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        print(f"\n{test_name}")
        print(f"  Query: {query_string}")
        print(f"  Sig:   {signature}")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("HMAC-SHA256 BINANCE API SIGNING GUIDE")
    print("="*80)
    
    demo_hmac_signing()
    compare_implementations()
    test_real_signature()
    
    print("\n\n" + "="*80)
    print("KEY TAKEAWAYS")
    print("="*80)
    print("""
1. ALWAYS use .hexdigest() to convert HMAC to hex string
2. ALWAYS encode both api_secret and query_string as UTF-8 bytes
3. ALWAYS use hashlib.sha256 (not md5, sha1, etc.)
4. ALWAYS sort query parameters by key name
5. ALWAYS include the timestamp parameter
6. ALWAYS append the signature to the request as a parameter

Example correct implementation:
    import hmac, hashlib, time
    
    timestamp = int(time.time() * 1000)
    query = f"timestamp={timestamp}"
    sig = hmac.new(api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
    
    # Use in request:
    params = {'timestamp': timestamp, 'signature': sig}
    requests.get(url, params=params, headers={'X-MBX-APIKEY': api_key})
    """)
    print("="*80 + "\n")

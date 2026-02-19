#!/usr/bin/env python3
"""
Guide to fix Binance API Key issues and generate new valid credentials.
"""

def show_guide():
    print("\n" + "=" * 70)
    print("🔧 BINANCE API KEY FIX GUIDE")
    print("=" * 70)
    
    print("""
The current API keys in .env are NOT working.
Follow these steps to get valid, working API keys:

═══════════════════════════════════════════════════════════════════════
STEP 1: Create Binance Testnet Account (RECOMMENDED FOR TESTING)
═══════════════════════════════════════════════════════════════════════

✅ This is the SAFEST option - you trade with fake money
   - No real funds at risk
   - Perfect for testing and development

1. Go to: https://testnet.binancefuture.com
2. Click "Sign Up" (or use existing Binance account)
3. Complete verification
4. Create API Key:
   a) Click "API" in settings
   b) Click "Create New Key"
   c) Label: "TradingBot" (optional)
   d) Enable: "Enable Spot & Margin Trading"
   e) Disable: "Enable Futures" (if not needed)
   f) Leave IP Whitelist EMPTY (or add your IP)
   g) Create & Download

5. Copy the API Key and Secret

═══════════════════════════════════════════════════════════════════════
STEP 2: Update Your .env File
═══════════════════════════════════════════════════════════════════════

Open .env and replace with your NEW keys:

   BINANCE_API_KEY=your_api_key_here
   BINANCE_API_SECRET=your_api_secret_here
   
⚠️  IMPORTANT:
   - Keys are CASE SENSITIVE
   - No extra spaces or quotes
   - Do NOT share these keys with anyone

═══════════════════════════════════════════════════════════════════════
STEP 3: Test Your New Keys
═══════════════════════════════════════════════════════════════════════

Run the test script:
   python test_api_keys.py

If successful, you'll see:
   ✅ SUCCESS: API keys are WORKING!

═══════════════════════════════════════════════════════════════════════
STEP 4: Choose Your Exchange Mode
═══════════════════════════════════════════════════════════════════════

In .env, set EXCHANGE_MODE to:

   • mock      → Use MockExchange (no API, completely offline)
   • ccxt      → Use CCXT with Binance (real API calls)
   • binance   → Use legacy REST API (not recommended)

Examples:
   EXCHANGE_MODE=mock           # For testing without API calls ✅
   EXCHANGE_MODE=ccxt           # For live API testing

═══════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════

❌ Error: "Invalid API-key"
   → Check if you copied the full key/secret correctly
   → Make sure there are no extra spaces

❌ Error: "IP not allowed"
   → Go to API settings in Binance
   → Leave "IP Whitelist" EMPTY to allow all IPs
   → Or add your current IP address

❌ Error: "Permission denied"
   → Check API key restrictions in Binance dashboard
   → Ensure "Enable Spot & Margin Trading" is enabled

❌ Key still not working?
   → Regenerate the key in Binance dashboard
   → Delete old key first
   → Create new key with proper permissions

═══════════════════════════════════════════════════════════════════════
QUICK START OPTIONS
═══════════════════════════════════════════════════════════════════════

Option A: TEST WITH MOCK (Recommended for now)
   1. Change: EXCHANGE_MODE=mock
   2. Run: python main.py test
   3. No API keys needed!

Option B: GET REAL BINANCE TESTNET KEYS
   1. Register at: https://testnet.binancefuture.com
   2. Generate API keys
   3. Update .env with new keys
   4. Run: python test_api_keys.py (to verify)
   5. Change: EXCHANGE_MODE=ccxt
   6. Run: python main.py market

═══════════════════════════════════════════════════════════════════════
SECURITY WARNING
═══════════════════════════════════════════════════════════════════════

⚠️  The API keys in your current .env are VISIBLE in code
    If these are REAL keys:
    1. Immediately DELETE them from Binance
    2. Generate NEW keys
    3. Never commit .env to git (add to .gitignore)
    4. Consider using environment variables instead

.gitignore should contain:
   .env
   *.local
   keys/
   secrets/

═══════════════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    show_guide()
    
    print("\n🎯 NEXT STEPS:")
    print("   1. Read the guide above carefully")
    print("   2. Get new API keys from Binance Testnet")
    print("   3. Update your .env file")
    print("   4. Run: python test_api_keys.py")
    print("\n" + "=" * 70)

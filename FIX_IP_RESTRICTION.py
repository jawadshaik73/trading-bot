#!/usr/bin/env python3
"""
Script to help configure API key restrictions and test with different endpoints.
"""
import os
import subprocess
import sys

def show_ip_fix_guide():
    print("\n" + "=" * 70)
    print("🔐 BINANCE API KEY - FIX IP RESTRICTION ISSUE")
    print("=" * 70)
    
    print("""
YOUR BINANCE API KEY SETTINGS HAVE A SECURITY ISSUE:

❌ Current Configuration (WILL BE DELETED):
   ├─ IP Restriction: Unrestricted (Less Secure)
   └─ Permissions: Multiple enabled (Trading, Withdrawals, etc.)

Binance AUTOMATICALLY DELETES such keys for security!

✅ SOLUTION: You have 2 options:

═══════════════════════════════════════════════════════════════════════
OPTION 1: RESTRICT TO YOUR IP (Recommended)
═══════════════════════════════════════════════════════════════════════

1. Go to: https://www.ipchicken.com/ (or google "my IP")
2. Copy your public IP address (e.g., 203.0.113.42)

3. Login to Binance: https://www.binance.com
4. Go to: Account Settings → API Management
5. Click on your API Key (jawad123)
6. Click "Edit Restrictions"
7. Under "IP access restrictions":
   ✅ Select "Restrict access to trusted IPs only"
   ✅ Add your IP: [YOUR_IP_HERE]
   ✅ Save

8. After restriction is set, your API key will WORK!

═══════════════════════════════════════════════════════════════════════
OPTION 2: USE TESTNET INSTEAD (Easiest)
═══════════════════════════════════════════════════════════════════════

For testing with fake money (safer):

1. Go to: https://testnet.binancefuture.com
2. Create a NEW API key with these settings:
   ├─ Enable: Spot & Margin Trading
   ├─ Disable: Withdrawals
   ├─ IP Restriction: Unrestricted OR your IP
   └─ Save

3. Update your .env:
   EXCHANGE_MODE=ccxt
   BINANCE_API_KEY=<testnet_key>
   BINANCE_API_SECRET=<testnet_secret>

═══════════════════════════════════════════════════════════════════════
YOUR CURRENT API KEY DETAILS
═══════════════════════════════════════════════════════════════════════

API Key: u3qx9E414tQMNeKOy6b3zc3tsssSYtdwzMnbkb7DkC231oyWSROiAfdCS7a8OjJ3
Status: ⚠️  WILL BE DELETED (Unrestricted + Trading permissions)

Enabled Permissions:
   ✅ Reading
   ✅ Spot & Margin Trading
   ✅ Margin Loan, Repay & Transfer
   ✅ Universal Transfer
   ✅ Withdrawals
   ✅ Symbol Whitelist

Required Fix:
   🔒 Add IP restriction: https://www.ipchicken.com/
   📋 Then test: python test_api_keys.py

═══════════════════════════════════════════════════════════════════════
DO THIS NOW (Step by Step)
═══════════════════════════════════════════════════════════════════════

Step 1: Find your IP
   → Go to: https://www.ipchicken.com/
   → Copy the IP address shown (e.g., 221.120.50.100)

Step 2: Update Binance API settings
   → Login: https://www.binance.com
   → Account Settings → API Management
   → Find "jawad123" API key
   → Click "Edit Restrictions"
   → IP restrictions: Check "Restrict access"
   → Add IP: [PASTE_YOUR_IP]
   → Save & Confirm

Step 3: Test the API key
   → Run: python test_api_keys.py
   → You should see: ✅ SUCCESS: API keys are WORKING!

Step 4: Start using the bot
   → Update .env: EXCHANGE_MODE=ccxt
   → Run: python main.py market

═══════════════════════════════════════════════════════════════════════
IMPORTANT: DO THIS WITHIN 24 HOURS!
═══════════════════════════════════════════════════════════════════════

⚠️  Binance will DELETE your API key if:
   - IP is unrestricted AND
   - Any permission other than Reading is enabled

Your key matches this criteria, so it will be deleted soon!

Fix it NOW to keep your key working.

═══════════════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    show_ip_fix_guide()
    
    print("\n📌 QUICK CHECKLIST:")
    print("   ☐ Find my IP at https://www.ipchicken.com/")
    print("   ☐ Login to Binance")
    print("   ☐ Go to API Management")
    print("   ☐ Edit my 'jawad123' key restrictions")
    print("   ☐ Add IP restriction with my IP")
    print("   ☐ Save & Confirm")
    print("   ☐ Run: python test_api_keys.py")
    print("   ☐ Update EXCHANGE_MODE=ccxt in .env")
    print("   ☐ Run bot: python main.py market")
    print("\n" + "=" * 70)

#!/usr/bin/env python3
"""
Automated API Key Setup and Verification
Helps configure and test your Binance API key
"""
import os
import sys
from dotenv import load_dotenv

def get_current_ip():
    """Try to detect current IP address"""
    try:
        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return "Unable to detect"

def show_setup_instructions():
    print("\n" + "=" * 70)
    print("🚀 BINANCE API KEY - COMPLETE SETUP GUIDE")
    print("=" * 70)
    
    current_ip = get_current_ip()
    
    print(f"""
YOUR PRIVATE IP (Local): {current_ip}
(You need your PUBLIC IP, not this one)

═══════════════════════════════════════════════════════════════════════
IMMEDIATE ACTION REQUIRED (URGENT)
═══════════════════════════════════════════════════════════════════════

Your Binance API key has unrestricted IP access with trading
permissions. Binance WILL DELETE IT for security reasons!

⏰ FIX WITHIN 24 HOURS or your key will be DELETED!

═══════════════════════════════════════════════════════════════════════
STEP 1: GET YOUR PUBLIC IP ADDRESS
═══════════════════════════════════════════════════════════════════════

Go to one of these websites (they show your public IP):
   • https://www.ipchicken.com/
   • https://whatismyipaddress.com/
   • https://www.my-ip.io/

Copy the IP address shown (looks like: 203.0.113.42)

═══════════════════════════════════════════════════════════════════════
STEP 2: ADD IP RESTRICTION IN BINANCE
═══════════════════════════════════════════════════════════════════════

1. Go to: https://www.binance.com
2. Login with your account
3. Click: User Icon (top right) → Account
4. Find: API Management
5. Find your key labeled: "jawad123"
6. Click: "Edit Restrictions"
7. Under "IP access restrictions":
   • UNCHECK: "Unrestricted"
   • CHECK: "Restrict access to trusted IPs only"
   • Click: "Add IP"
   • Paste: Your public IP from Step 1
   • Make sure to include /32 (e.g., 203.0.113.42/32)
8. Under "Restriction Scope":
   • Make sure "Reading" is enabled
   • Make sure "Spot & Margin Trading" is enabled
9. Click: "Save" or "Confirm"

✅ Your API key will now work!

═══════════════════════════════════════════════════════════════════════
STEP 3: VERIFY API KEY IS WORKING
═══════════════════════════════════════════════════════════════════════

After you've restricted the IP, run this test:

    python test_api_keys.py

Expected output:
    ✅ SUCCESS: API keys are WORKING!

═══════════════════════════════════════════════════════════════════════
STEP 4: ENABLE LIVE API IN YOUR BOT
═══════════════════════════════════════════════════════════════════════

Edit your .env file and change:

    From: EXCHANGE_MODE=mock
    To:   EXCHANGE_MODE=ccxt

Then run the bot:

    python main.py market

═══════════════════════════════════════════════════════════════════════
REFERENCE: YOUR API KEY DETAILS
═══════════════════════════════════════════════════════════════════════

API Key (in .env):     u3qx9E414tQMNeKOy6b3zc3tsssSYtdwzMnbkb7DkC231oyWSROiAfdCS7a8OjJ3
API Label:             jawad123
Permissions:           ✅ Reading, Trading, Withdrawals
Current IP Limit:      ❌ Unrestricted (MUST FIX!)
Status:                ⚠️  Will be deleted if not fixed within 24 hours

═══════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════

❌ "Invalid API-key"
   → Make sure you entered the CORRECT IP in Binance
   → Make sure it includes /32 at the end (203.0.113.42/32)
   → You may need to wait 5 minutes after saving

❌ "IP not allowed"
   → Your IP might have changed
   → Check your public IP again at ipchicken.com
   → Update it in Binance API settings

❌ Still not working?
   → Wait 10 minutes for Binance to update
   → Try again: python test_api_keys.py
   → If still failing, contact Binance support

═══════════════════════════════════════════════════════════════════════
SAFETY REMINDER
═══════════════════════════════════════════════════════════════════════

⚠️  Your API credentials are EXPOSED in .env file
    If these are REAL account keys:
    1. Add .env to .gitignore
    2. Never commit to public repositories
    3. Consider regenerating keys if shared

Consider creating dedicated API keys:
    • One for testing (MOCK mode)
    • One for production (with IP restrictions)
    • Both with minimal required permissions

═══════════════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    show_setup_instructions()
    print("✅ Setup Guide Complete")
    print("=" * 70)

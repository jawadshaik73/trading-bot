#!/usr/bin/env python3
"""
BINANCE API SECURITY CHECKLIST & CONFIGURATION GUIDE
Comprehensive security recommendations for your trading bot API key
"""

print("""
═══════════════════════════════════════════════════════════════════════════════
BINANCE API SECURITY & CONFIGURATION GUIDE
═══════════════════════════════════════════════════════════════════════════════

Your API Key: jawad123
Current Status: ❌ FAILING (Missing permissions + IP mismatch)
Security Risk: ⚠️ MODERATE (API key has broad permissions, needs hardening)

═══════════════════════════════════════════════════════════════════════════════
PART 1: API PERMISSIONS FOR TRADING BOT (REQUIRED)
═══════════════════════════════════════════════════════════════════════════════

✅ MUST ENABLE FOR BOT TO WORK:
───────────────────────────────

1. ☑ Enable Reading
   └─ Required: View account balance, orders, positions
   
2. ☑ Enable Spot & Margin Trading  
   └─ Required: Place/cancel orders
   
3. ☑ Enable Futures
   └─ CRITICAL! For futures trading
   
4. ☑ Enable Futures Algorithm Trading
   └─ Required: Advanced order types

❌ DO NOT NEED FOR BOT:
───────────────────────
- Withdrawals (bot doesn't withdraw)
- Margin Loan, Repay & Transfer (unless using margin)
- Universal Transfer (unless moving between accounts)


═══════════════════════════════════════════════════════════════════════════════
PART 2: IP WHITELIST CONFIGURATION (CRITICAL)
═══════════════════════════════════════════════════════════════════════════════

CURRENT ISSUE:
├─ Whitelisted IP: 157.50.130.184 ❌ OLD (not working)
├─ Your Current IP: 106.215.168.255 ✅ NEW (needs to be added)
└─ Status: IP MISMATCH → Error -2015

🔧 TO FIX:
────────
1. Go to: https://www.binance.com/en/usercenter/settings/api-management
2. Click jawad123 → Edit Restrictions
3. Select: "Restrict access to trusted IPs only" (RECOMMENDED)
4. Delete: 157.50.130.184
5. Add: 106.215.168.255
6. Save & wait 30 seconds

⚠️  SECURITY TIP:
────────────────
Never use "Unrestricted" unless absolutely necessary!
Always whitelist specific IPs for safety.

To check your IP dynamically:
  curl https://api.ipify.org


═══════════════════════════════════════════════════════════════════════════════
PART 3: WITHDRAWAL SETTINGS (NOT NEEDED FOR BOT)
═══════════════════════════════════════════════════════════════════════════════

Current Status:
├─ Withdrawal Whitelist: OFF
├─ One-step Withdrawal: OFF
└─ Off-chain Withdrawal: N/A

For TRADING BOT, withdrawal settings are NOT required because:
✓ Bot only places orders
✓ Bot doesn't withdraw funds
✓ Funds stay in your account
✓ No API key withdrawal permissions needed

HOWEVER - For GENERAL SECURITY (if you plan to withdraw):

If Withdrawal Whitelist is OFF:
  └─ You can withdraw to ANY address (less secure)

If Withdrawal Whitelist is ON:
  └─ You can only withdraw to pre-approved addresses (MORE SECURE)

RECOMMENDATION:
If you plan to work with real funds:
  1. Enable Withdrawal Whitelist
  2. Add only your personal wallet addresses
  3. This prevents accidental withdrawals to wrong addresses


═══════════════════════════════════════════════════════════════════════════════
PART 4: COMPLETE SECURITY CONFIGURATION CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

FOR TRADING BOT - MINIMUM REQUIRED:
───────────────────────────────────
☑ API Key Name: jawad123
☑ Enable Reading
☑ Enable Spot & Margin Trading  
☑ Enable Futures
☑ Enable Futures Algorithm Trading
☑ IP Restriction: Whitelist ONLY 106.215.168.255
☐ Withdrawals: NOT needed (leave OFF)
☐ Margin Loan: NOT needed (leave OFF)
☐ Universal Transfer: NOT needed (leave OFF)


FOR ADVANCED SECURITY (RECOMMENDED):
────────────────────────────────────
1. Account Security:
   ☑ Enable 2FA (Two-Factor Authentication)
   ☑ Enable SMS/Email notifications for logins
   ☑ Enable withdrawal confirmation emails

2. API Key Security:
   ☑ Use SEPARATE API keys for different purposes
      - Key 1: Trading (jawad123) - ENABLE: Reading, Spot, Futures
      - Key 2: ReadOnly (if needed) - ENABLE: Reading only
   ☑ Rotate API keys regularly (every 3-6 months)
   ☑ Set API key expiration date if possible

3. IP Whitelist Strategy:
   ☑ Whitelist ONLY your home/office IP
   ☑ If IP changes (mobile, VPN), update immediately
   ☑ Never use "Unrestricted" unless testing locally
   ☑ Monitor: https://api.ipify.org for your current IP

4. Withdrawal Security (if using real funds):
   ☑ Enable Withdrawal Whitelist
   ☑ Add ONLY your personal wallet addresses
   ☑ Enable withdrawal confirmation via email/SMS
   ☑ Use long withdrawal delay (e.g., 2-24 hours)

5. Monitoring:
   ☑ Check "API key usage history" regularly
   ☑ Review IP access logs
   ☑ Set up alerts for unusual activity


═══════════════════════════════════════════════════════════════════════════════
PART 5: STEP-BY-STEP SECURITY SETUP
═══════════════════════════════════════════════════════════════════════════════

STEP 1: Update Existing "jawad123" API Key
───────────────────────────────────────────
1. Visit: https://www.binance.com/en/usercenter/settings/api-management
2. Find: "jawad123" API key
3. Click: Pencil icon (Edit)
4. Go to: Restrictions section

   Permissions (Enable these):
   ✓ Enable Reading
   ✓ Enable Spot & Margin Trading
   ✓ Enable Futures
   ✓ Enable Futures Algorithm Trading
   
   Permissions (Disable these):
   ✗ Withdrawals (NOT needed)
   ✗ Margin Loan, Repay & Transfer (NOT needed)
   ✗ Universal Transfer (NOT needed)
   
   IP Whitelist (Very Important):
   → Delete: 157.50.130.184
   → Add: 106.215.168.255
   
5. Click: Save Changes
6. Wait: 30+ seconds for propagation


STEP 2: Optional - Create Additional API Key (Advanced)
───────────────────────────────────────────────────────
For maximum security, create separate keys:

Key 1 - "TradingBot" (for trading):
  ✓ Enable Reading
  ✓ Enable Spot & Margin Trading
  ✓ Enable Futures
  ✓ IP: 106.215.168.255
  ✗ Withdrawals disabled

Key 2 - "Monitor-ReadOnly" (for monitoring):
  ✓ Enable Reading only
  ✗ All trading disabled
  ✓ IP: Any (for monitoring from phone)

→ Use only Key 1 for your trading bot
→ Use Key 2 for checking balances from mobile


STEP 3: Account-Level Security (Highly Recommended)
────────────────────────────────────────────────────
1. Enable 2FA:
   https://www.binance.com/en/usercenter/security/
   → Use Google Authenticator or Microsoft Authenticator
   → DO NOT use SMS 2FA (less secure)
   → BACKUP your 2FA secret key in a safe place!

2. Email Security:
   → Verify email is correct and only you have access
   → Enable withdrawal confirmation emails

3. Withdrawal Whitelist (if handling real funds):
   https://www.binance.com/en/usercenter/withdrawal
   → Enable "Withdrawal Whitelist"
   → Add only your personal wallet addresses
   → Test with small amount first


STEP 4: Verify Everything Works
────────────────────────────────
1. Save changes
2. Wait 30 seconds
3. Run test:
   python QUICK_API_TEST.py
   
Expected output:
   ✅ SUCCESS! API is working!


═══════════════════════════════════════════════════════════════════════════════
PART 6: COMMON SECURITY MISTAKES TO AVOID
═══════════════════════════════════════════════════════════════════════════════

❌ MISTAKE 1: Using "Unrestricted" IP
   Problem: Anyone anywhere can use your API key
   Fix: Always whitelist specific IPs only

❌ MISTAKE 2: Mixing testnet and mainnet keys
   Problem: Could accidentally trade with real money
   Fix: Use clearly labeled keys (mainnet key, testnet key)

❌ MISTAKE 3: Enabling withdrawal permission unnecessarily
   Problem: If key is compromised, funds can be stolen
   Fix: Only enable what you need (trading only)

❌ MISTAKE 4: Using same IP whitelist for all keys
   Problem: All keys compromised if one IP is leaked
   Fix: Use different IPs for different keys if possible

❌ MISTAKE 5: Forgetting to rotate API keys
   Problem: Older compromised keys stay active
   Fix: Delete old keys and create new ones every 6 months

❌ MISTAKE 6: Not backing up 2FA secret
   Problem: Can't recover account if phone is lost
   Fix: Store 2FA backup code in secure location


═══════════════════════════════════════════════════════════════════════════════
PART 7: PERMISSION REFERENCE TABLE
═══════════════════════════════════════════════════════════════════════════════

Permission | Bot Needs | Default | Recommendation
─────────────────────────────────────────────────────────────────────────────
Reading | YES | OFF | ☑ ENABLE
Spot Trading | MAYBE | OFF | ☑ ENABLE if trading spot
Margin Trading | MAYBE | OFF | ☑ ENABLE if using margin
Margin Loan | NO | OFF | ☐ LEAVE OFF
Futures | YES | OFF | ☑ ENABLE (your bot uses futures)
Algo Trading | YES | OFF | ☑ ENABLE (for advanced orders)
Universal Transfer | NO | OFF | ☐ LEAVE OFF
Withdrawals | NO | OFF | ☐ LEAVE OFF (IMPORTANT!)
IP Whitelist | YES | N/A | ✓ SET TO 106.215.168.255
2FA | RECOMMENDED | OFF | ☑ ENABLE for account security


═══════════════════════════════════════════════════════════════════════════════
PART 8: WHAT HAPPENS AFTER CONFIGURATION
═══════════════════════════════════════════════════════════════════════════════

After you configure everything correctly:

1. IMMEDIATE (within 30 seconds):
   ✓ IP whitelist takes effect
   ✓ New permissions are active
   ✓ API test should pass

2. SHORT TERM (next few minutes):
   ✓ Try trading small amount
   ✓ Verify orders execute correctly
   ✓ Check that cancellations work

3. LONG TERM (ongoing):
   ✓ Monitor API usage logs monthly
   ✓ Check for unauthorized IP access attempts
   ✓ Rotate API keys every 6 months
   ✓ Update IP whitelist if IP changes


═══════════════════════════════════════════════════════════════════════════════
PART 9: TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

ERROR: Still getting -2015 error after enabling permissions
────────────────────────────────────────────────────────────
1. Verify you clicked "Save Changes"
2. Wait full 30 seconds (browser may need refresh)
3. Clear browser cache and reload
4. Try from different browser
5. Contact Binance support if persists

ERROR: API key works but orders fail
──────────────────────────────────────
1. Check "Enable Futures" is checked
2. Verify account has sufficient balance
3. Check order parameters (symbol, quantity, price)
4. Review Binance API documentation

ERROR: Shows as "Unrestricted" even after setting IP
──────────────────────────────────────────────────────
1. Refresh page (Ctrl+Shift+R)
2. Try different browser
3. Clear cookies and login again
4. Contact Binance support


═══════════════════════════════════════════════════════════════════════════════
FINAL CHECKLIST BEFORE USING BOT
═══════════════════════════════════════════════════════════════════════════════

Security Checklist:
☐ "Enable Futures" is ☑ CHECKED
☐ "Enable Reading" is ☑ CHECKED  
☐ "Enable Spot & Margin Trading" is ☑ CHECKED
☐ IP Whitelist is set to: 106.215.168.255
☐ Withdrawals permission is ☐ UNCHECKED (disabled)
☐ At least 30 seconds have passed since saving

Functionality Checklist:
☐ python QUICK_API_TEST.py returns ✅ SUCCESS
☐ Account balance displays correctly
☐ Can place test orders
☐ Can cancel test orders

Safety Checklist:
☐ 2FA (Google Authenticator) is enabled on account
☐ Email verification enabled for withdrawals
☐ Withdrawal whitelist is enabled (if applicable)
☐ Using small amounts for testing first
☐ Have backup of 2FA secret key

═══════════════════════════════════════════════════════════════════════════════
QUICK SUMMARY
═══════════════════════════════════════════════════════════════════════════════

For your trading bot to work:
1. ☑ Enable: Reading, Spot Trading, Futures, Algo Trading
2. ☑ Whitelist IP: 106.215.168.215
3. ☐ Disable: Withdrawals (NOT needed)
4. ☐ Ignore: Withdrawal whitelist (NOT needed for bot)
5. Test: python QUICK_API_TEST.py

For maximum security:
1. Enable 2FA on your Binance account
2. Whitelist withdrawal addresses
3. Monitor API logs regularly
4. Rotate keys every 6 months

═══════════════════════════════════════════════════════════════════════════════
""")

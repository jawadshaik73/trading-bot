# API KEY FIX GUIDE - CRITICAL ISSUES FOUND

## Current Status
✓ **HMAC-SHA256 Implementation: CORRECT**
✗ **API Authentication: FAILING (-2015 error)**

## Root Causes Identified

### 1. IP Address Mismatch
- **Your Current Public IP:** `106.215.168.255`
- **Whitelisted IP in Settings:** `157.50.130.184`
- **Status:** ❌ These don't match!

### 2. Possible Missing Permissions
- **Enable Futures:** Unknown (likely not enabled)
- **Enable Spot & Margin Trading:** Unknown (likely not enabled)

---

## IMMEDIATE FIXES REQUIRED

### Fix #1: Update Binance API Key Settings (MUST DO)

**Steps:**
1. Go to: https://www.binance.com/en/usercenter/settings/api-management
2. Find and click on API key named `jawad123`
3. Click **Edit Restrictions**
4. **Enable these permissions:**
   - ☑ Enable Reading
   - ☑ Enable Spot & Margin Trading
   - ☑ Enable Futures (CRITICAL!)
   - ☑ Enable Future Algorithm Trading
5. **Update IP Whitelist:**
   - Option A (Recommended for testing): Select **"Unrestricted"** temporarily
   - Option B (More Secure): Add your current IP: `106.215.168.255`
6. Click **Save Changes**
7. **Wait 30 seconds** for changes to take effect

### Fix #2: Test the API After Changes

Run this test after updating settings:
```bash
python DIAGNOSE_API_ISSUE.py
```

---

## Alternative Solution: Use Mock Mode (No API Keys Needed)

If you don't want to fix the API keys right now, you can continue using mock mode:

**Current setting in .env:**
```
EXCHANGE_MODE=mock
```

This is safe and allows you to:
- Test bot strategies offline
- No real money at risk
- No API key issues

Switch when you're ready to trade with real API.

---

## HMAC-SHA256 Implementation Reference

Your HMAC implementation is **CORRECT**. Here's what's being used:

```python
import hmac
import hashlib

def generate_signature(api_secret, query_string):
    return hmac.new(
        api_secret.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

# Example usage:
# query_string = "timestamp=1234567890&symbol=BTCUSDT"
# signature = generate_signature(api_secret, query_string)
```

**Key points:**
- ✓ Using `hmac.new()` with API secret
- ✓ Using `hashlib.sha256`
- ✓ Encoding both secret and query string as UTF-8
- ✓ Using `.hexdigest()` to get the hex string

---

## Step-by-Step IP Whitelist Update

Since your IP changed:

1. **Detect current IP:** `106.215.168.255`
2. **Update Binance API Settings:**
   - Visit: https://www.binance.com/en/usercenter/settings/api-management
   - Click pencil icon next to `jawad123` API key
   - Scroll to "IP access restrictions"
   - Click **"Edit Restrictions"**
   - Select **"Restrict access to trusted IPs only"**
   - Clear old IP `157.50.130.184`
   - Add new IP: `106.215.168.255`
   - Click Save
3. **Wait 30+ seconds** for propagation

---

## Configuration Checklist

Before switching from mock mode, ensure:

- [ ] API Key: `Xezi07XwsWqk79I27ZjkIFlDiHczbd1EvuEQBEI0nNvfqET3bc7FnVErtrLnH9in`
- [ ] API Secret: `Ds4DgM0FRCvWtBfQY4te1ixCCQGWiEzhrj0Zf7ChJfrmLfJsNk5IeFuZ6B1AYWdP`
- [ ] "Enable Futures" ✓ CHECKED
- [ ] "Enable Spot & Margin Trading" ✓ CHECKED
- [ ] IP Whitelisted: `106.215.168.255` or Unrestricted
- [ ] Waited 30+ seconds after saving
- [ ] Test with DIAGNOSE_API_ISSUE.py passes

---

## To Enable Real Trading (After Fixes Applied)

Edit your `.env` file:

```dotenv
# Change this:
EXCHANGE_MODE=mock

# To this:
EXCHANGE_MODE=ccxt

# Keep sandbox mode enabled until you're confident:
CCXT_SANDBOX_MODE=True
```

Then restart and test:
```bash
python cli.py info
```

---

## If You Still Get -2015 Error

**Try these:**
1. Verify API Key/Secret in `.env` are copied **exactly** (no extra spaces)
2. Make sure you're using **Mainnet** keys (not Testnet)
3. Disable IP restriction temporarily: Set to "Unrestricted"
4. Wait 5 minutes for Binance to sync changes
5. Check browser: https://api.ipify.org to confirm your current IP
6. Run test again with `python DIAGNOSE_API_ISSUE.py`


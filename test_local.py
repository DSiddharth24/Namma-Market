"""
Namma Market — Local Test Script
Run this BEFORE setting up Twilio/ngrok to verify all features work correctly.
Usage: python test_local.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 55)
print("  NAMMA MARKET — LOCAL FEATURE TEST")
print("=" * 55)

# ── 1. Environment check ──────────────────────────────────
print("\n📋 STEP 1: Environment Check")
keys = {
    "GEMINI_API_KEY":     os.getenv("GEMINI_API_KEY", ""),
    "TWILIO_ACCOUNT_SID": os.getenv("TWILIO_ACCOUNT_SID", ""),
    "TWILIO_AUTH_TOKEN":  os.getenv("TWILIO_AUTH_TOKEN", ""),
}
all_set = True
for name, val in keys.items():
    if val and not val.startswith("your_") and not val.startswith("ACxxxx") and not val.startswith("sk-xxx"):
        print(f"  ✅ {name} — set")
    else:
        print(f"  ❌ {name} — NOT SET (edit your .env file)")
        all_set = False

if not all_set:
    print("\n⚠️  Fill in .env before full testing. Continuing with available features...\n")

# ── 2. APMC rates (no API key needed for layers 1 + 3) ───
print("\n📊 STEP 2: APMC Rate Fetching")
from services.apmc_service import fetch_apmc_rates, format_rates_message

crops_to_test = ["sugarcane", "ರಾಗಿ", "tomato", "ಅಡಿಕೆ"]
for crop in crops_to_test:
    result = fetch_apmc_rates(crop)
    msg = format_rates_message(result, crop)
    first_line = msg.split("\n")[0]
    print(f"  ✅ '{crop}' → {result['status']} | {len(result.get('records', []))} records | {first_line[:50]}")

# ── 3. Full conversation flow simulation ─────────────────
print("\n💬 STEP 3: Conversation Flow Simulation")
from services.ai_agent import handle_message

PHONE = "+919999999999"   # fake test number

scenarios = [
    ("Greeting",          "hi"),
    ("APMC Kannada",      "ಕಬ್ಬು ದರ ತಿಳಿಸಿ"),
    ("APMC English",      "today tomato price mandya"),
    ("Schemes menu",      "government schemes"),
    ("Eligibility start", "pm kisan eligibility check"),
    ("Fertilizer advice", "sugarcane fertilizer"),
    ("Loan info",         "kcc loan details"),
    ("All APMC rates",    "all rates"),
]

for label, msg in scenarios:
    try:
        resp = handle_message(PHONE, msg)
        preview = resp.replace("\n", " ")[:70]
        print(f"  ✅ [{label}] → {preview}...")
    except Exception as e:
        print(f"  ❌ [{label}] ERROR: {e}")

# ── 4. Eligibility engine ─────────────────────────────────
print("\n✅ STEP 4: Eligibility Engine")
from services.eligibility_engine import check_scheme_eligibility

tests = [
    ("pm_kisan",   {"land_owner": "yes", "income_tax": "no", "govt_employee": "no", "aadhaar": "yes"}, True),
    ("pm_kisan",   {"land_owner": "yes", "income_tax": "yes", "govt_employee": "no", "aadhaar": "yes"}, False),
    ("kcc",        {"age": "35", "land_area": "3 acres", "existing_loan": "no", "bank_account": "yes"}, True),
    ("drip_sprinkler", {"land_area": "2 acres", "water_source": "yes", "category": "general"}, True),
    ("drip_sprinkler", {"land_area": "0.2 acres", "water_source": "yes", "category": "general"}, False),
]

for scheme, answers, expected in tests:
    result = check_scheme_eligibility(scheme, answers)
    status = "✅" if result["eligible"] == expected else "❌"
    print(f"  {status} {scheme} | eligible={result['eligible']} (expected {expected})")

# ── 5. Summary ────────────────────────────────────────────
print("\n" + "=" * 55)
print("  TEST COMPLETE")
print("=" * 55)
print("""
Next steps to test on WhatsApp:
  1. Fill in .env with your real keys
  2. Run:  python app.py
  3. Run:  ngrok http 5000
  4. Copy the ngrok URL (https://xxxx.ngrok.io)
  5. Set Twilio sandbox webhook to:
     https://xxxx.ngrok.io/webhook/whatsapp
  6. WhatsApp the sandbox join code to +1 415 523 8886
  7. Send any message — the bot will reply!

Twilio Sandbox:  https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
""")

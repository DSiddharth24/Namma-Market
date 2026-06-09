"""
Namma Market AI Agent — powered by Google Gemini (FREE tier)

Key fixes:
- Active flow ALWAYS takes priority over intent detection
- Main menu numbers (1-5) handled before anything else
- "loan" keyword takes priority over "scheme"
- Scheme info displayed directly (not via GPT) when scheme name typed
- Crop names in context of eligibility/scheme don't trigger fertilizer flow
- GPT only fires for truly unrecognised messages
"""

import os
from google import genai
from google.genai import types

from services.session_manager import get_session, save_session, update_session, clear_session
from services.apmc_service import fetch_apmc_rates, format_rates_message, CROP_ALIASES
from services.eligibility_engine import check_scheme_eligibility
from data.schemes import SCHEMES, BANK_LOANS
from data.fertilizer_shops import FERTILIZER_SHOPS, CROP_ADVICE
import random

# ─────────────────────────────────────────────
# Gemini client — lazy init
# ─────────────────────────────────────────────
_gemini_client = None

def _get_client():
    global _gemini_client
    if _gemini_client is None:
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY not set.")
        _gemini_client = genai.Client(api_key=api_key)
    return _gemini_client


SYSTEM_PROMPT = """You are *Namma Market* 🌾, a friendly WhatsApp AI assistant for farmers in Mandya district, Karnataka, India.

Your personality:
- Warm, respectful, helpful — like a knowledgeable friend at the village market
- ALWAYS respond in BOTH English AND Kannada (ಕನ್ನಡ). Kannada after English.
- Simple language. Ask ONE follow-up question before giving advice.
- Add relevant emojis for WhatsApp readability.

Your expertise: APMC rates, govt schemes, eligibility, farm loans, crop/fertilizer advice for Mandya.

Rules:
- Always mention Mandya-specific contacts when relevant.
- For schemes/loans: official info with real helpline numbers.
- For fertilizer advice: always recommend a local Mandya shop.
- Keep responses under 1000 characters when possible.

Format: *bold* for important words, emojis, short bullet points."""


# ─────────────────────────────────────────────
# MAIN HANDLER — flow takes priority over intent
# ─────────────────────────────────────────────

def handle_message(phone: str, message: str) -> str:
    session = get_session(phone)
    msg = message.strip()
    msg_lower = msg.lower()
    current_flow = session.get("current_flow")

    # ── 1. ACTIVE FLOWS always win — don't re-detect intent ──────────────
    if current_flow == "apmc_followup":
        return _handle_apmc_followup(phone, msg, session)

    if current_flow == "scheme_eligibility_flow":
        return _handle_eligibility_flow(phone, msg, session)

    if current_flow == "fertilizer_flow":
        return _handle_fertilizer_flow(phone, msg, session)

    if current_flow == "loan_flow":
        return _handle_loan_flow(phone, msg, session)

    if current_flow == "scheme_info_flow":
        return _handle_scheme_info_flow(phone, msg, session)

    # ── 2. MAIN MENU numbers (1–5) ────────────────────────────────────────
    if msg.strip() in ("1", "2", "3", "4", "5"):
        menu_map = {
            "1": "apmc",
            "2": "scheme",
            "3": "eligibility",
            "4": "loan",
            "5": "fertilizer",
        }
        return _route_intent(phone, msg, session, menu_map[msg.strip()])

    # ── 3. GREETINGS / restart ────────────────────────────────────────────
    greeting_words = ["hi", "hello", "start", "ನಮಸ್ಕಾರ", "namaskara", "hey",
                      "namma market", "menu", "help", "ಸಹಾಯ"]
    if any(msg_lower == g or msg_lower.startswith(g + " ") for g in greeting_words) \
            or (len(msg_lower) <= 4 and msg_lower not in CROP_ALIASES):
        clear_session(phone)
        return _greeting_message()

    # ── 4. DETECT INTENT (only if no active flow) ─────────────────────────
    intent = _detect_intent(msg_lower)
    return _route_intent(phone, msg, session, intent)


def _route_intent(phone: str, msg: str, session: dict, intent: str) -> str:
    if intent == "apmc":
        return _start_apmc_flow(phone, msg, session)
    elif intent == "scheme":
        return _start_scheme_flow(phone, msg, session)
    elif intent == "eligibility":
        return _start_eligibility_selection(phone, msg, session)
    elif intent == "loan":
        return _start_loan_flow(phone, msg, session)
    elif intent == "fertilizer":
        return _start_fertilizer_flow(phone, msg, session)
    else:
        return _call_gemini(phone, msg, session)


# ─────────────────────────────────────────────
# INTENT DETECTION — loan beats scheme, specific beats general
# ─────────────────────────────────────────────

def _detect_intent(msg: str) -> str:
    # Loan FIRST — before scheme (since "loan scheme" should go to loan)
    loan_keywords = ["loan", "ಸಾಲ", "kcc", "credit card", "borrow",
                     "farm loan", "crop loan", "term loan", "finance"]
    if any(k in msg for k in loan_keywords):
        return "loan"

    # APMC / market rates
    rate_keywords = ["rate", "price", "ದರ", "ಬೆಲೆ", "apmc", "mandi",
                     "market rate", "today price", "ಇಂದಿನ ದರ", "ಮಾರ್ಕೆಟ್ ದರ"]
    if any(k in msg for k in rate_keywords):
        return "apmc"

    # Eligibility check
    eligibility_keywords = ["eligible", "ಅರ್ಹ", "qualify", "eligibility",
                            "check eligibility", "am i eligible"]
    if any(k in msg for k in eligibility_keywords):
        return "eligibility"

    # Specific scheme names → scheme info flow
    scheme_name_keywords = ["pm kisan", "pmkisan", "pmfby", "fasal bima",
                            "raita siri", "ರೈತ ಸಿರಿ", "soil health",
                            "ಮಣ್ಣು ಆರೋಗ್ಯ", "drip subsidy", "sprinkler subsidy",
                            "crop insurance", "ಬೆಳೆ ವಿಮೆ"]
    if any(k in msg for k in scheme_name_keywords):
        return "scheme_direct"

    # General scheme/government keywords
    scheme_keywords = ["scheme", "ಯೋಜನೆ", "government", "ಸರ್ಕಾರ",
                       "subsidy", "ಸಹಾಯಧನ", "yojana"]
    if any(k in msg for k in scheme_keywords):
        return "scheme"

    # Fertilizer / crop advice — only when explicitly asked, NOT just crop name alone
    fertilizer_explicit = ["fertilizer", "ಗೊಬ್ಬರ", "urea", "dap", "npk",
                           "advice", "ಸಲಹೆ", "pest", "ಕೀಟ", "disease", "ರೋಗ",
                           "irrigation", "ನೀರಾವರಿ", "varieties", "ತಳಿ",
                           "crop advice", "farming advice", "ಕೃಷಿ ಸಲಹೆ"]
    if any(k in msg for k in fertilizer_explicit):
        return "fertilizer"

    # Crop name alone (without advice keywords) → ask what they need
    crop_only_keywords = ["sugarcane", "ಕಬ್ಬು", "paddy", "ಭತ್ತ", "ragi", "ರಾಗಿ",
                          "tomato", "ಟೊಮೆಟೊ", "coconut", "ತೆಂಗಿನ", "banana", "ಬಾಳೆ",
                          "onion", "ಈರುಳ್ಳಿ", "potato", "ಆಲೂ"]
    if any(k in msg for k in crop_only_keywords):
        return "crop_clarify"

    return "general"


# ─────────────────────────────────────────────
# GREETING
# ─────────────────────────────────────────────

def _greeting_message() -> str:
    return (
        "🌾 *ನಮಸ್ಕಾರ! Welcome to Namma Market!* 🌾\n"
        "Mandya ಜಿಲ್ಲೆಯ ರೈತರಿಗೆ ನಿಮ್ಮ ಸ್ವಂತ ಸಹಾಯಕ!\n"
        "Your personal farming assistant for Mandya district!\n\n"
        "ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ | I can help you with:\n\n"
        "1️⃣ 📊 *ಇಂದಿನ APMC ದರಗಳು* | Today's Market Rates\n"
        "2️⃣ 🏛️ *ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು* | Government Schemes\n"
        "3️⃣ ✅ *ಯೋಜನೆ ಅರ್ಹತೆ ತಿಳಿಯಿರಿ* | Check Eligibility\n"
        "4️⃣ 🏦 *ಕೃಷಿ ಸಾಲ ಮಾಹಿತಿ* | Farm Loan Info\n"
        "5️⃣ 🌿 *ಬೆಳೆ ಮತ್ತು ಗೊಬ್ಬರ ಸಲಹೆ* | Crop & Fertilizer Advice\n\n"
        "ಸಂಖ್ಯೆ ಕಳಿಸಿ (1-5) ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಟೈಪ್ ಮಾಡಿ\n"
        "Send a number (1-5) or just type your question 👆"
    )


# ─────────────────────────────────────────────
# CROP CLARIFY — crop name alone, ask what they need
# ─────────────────────────────────────────────

def _route_intent(phone: str, msg: str, session: dict, intent: str) -> str:
    if intent == "apmc":
        return _start_apmc_flow(phone, msg, session)
    elif intent == "scheme":
        return _start_scheme_flow(phone, msg, session)
    elif intent == "scheme_direct":
        return _handle_scheme_direct(phone, msg, session)
    elif intent == "eligibility":
        return _start_eligibility_selection(phone, msg, session)
    elif intent == "loan":
        return _start_loan_flow(phone, msg, session)
    elif intent == "fertilizer":
        return _start_fertilizer_flow(phone, msg, session)
    elif intent == "crop_clarify":
        return _crop_clarify(phone, msg, session)
    else:
        return _call_gemini(phone, msg, session)


def _crop_clarify(phone: str, msg: str, session: dict) -> str:
    """Farmer typed just a crop name — ask what they need."""
    crop = msg.strip()
    update_session(phone, {"pending_crop": crop, "current_flow": None})
    return (
        f"🌾 *{crop.title()}* — ನಿಮಗೆ ಏನು ಬೇಕು? | What do you need?\n\n"
        f"1️⃣ 📊 ಇಂದಿನ ಮಾರ್ಕೆಟ್ ದರ | Today's market price\n"
        f"2️⃣ 🌿 ಗೊಬ್ಬರ ಮತ್ತು ಕೃಷಿ ಸಲಹೆ | Fertilizer & farming advice\n\n"
        f"1 ಅಥವಾ 2 ಕಳಿಸಿ | Send 1 or 2"
    )


# ─────────────────────────────────────────────
# APMC FLOW
# ─────────────────────────────────────────────

def _start_apmc_flow(phone: str, message: str, session: dict) -> str:
    msg_lower = message.lower()

    # Check if pending_crop exists from clarify step
    pending = session.get("pending_crop", "")
    if message.strip() == "1" and pending:
        crop = pending
        update_session(phone, {"current_flow": None, "pending_crop": ""})
        result = fetch_apmc_rates(commodity=crop)
        return format_rates_message(result, commodity=crop) + (
            "\n\n🌾 ಬೇರೆ ಬೆಳೆ ದರ ಬೇಕೇ? ಬೆಳೆ ಹೆಸರು ಟೈಪ್ ಮಾಡಿ.\n"
            "Need rates for another crop? Type the crop name."
        )

    # Try to extract crop from the message
    crop_mentioned = None
    for alias in CROP_ALIASES:
        if alias in msg_lower:
            crop_mentioned = alias
            break

    if crop_mentioned:
        result = fetch_apmc_rates(commodity=crop_mentioned)
        update_session(phone, {"current_flow": None})
        return format_rates_message(result, commodity=crop_mentioned) + (
            "\n\n🌾 ಬೇರೆ ಬೆಳೆ ದರ ಬೇಕೇ? ಬೆಳೆ ಹೆಸರು ಟೈಪ್ ಮಾಡಿ.\n"
            "Need rates for another crop? Type the crop name."
        )

    # No crop mentioned — ask which crop
    update_session(phone, {"current_flow": "apmc_followup"})
    return (
        "📊 *APMC ದರಗಳು | Market Rates*\n\n"
        "ಯಾವ ಬೆಳೆಯ ದರ ತಿಳಿಯಬೇಕು?\n"
        "Which crop rate do you want?\n\n"
        "• ಕಬ್ಬು (Sugarcane)  • ಭತ್ತ (Paddy)\n"
        "• ರಾಗಿ (Ragi)  • ಟೊಮೆಟೊ (Tomato)\n"
        "• ಅಡಿಕೆ (Arecanut)  • ತೆಂಗಿನಕಾಯಿ (Coconut)\n\n"
        "*all* ಎಂದು ಟೈಪ್ ಮಾಡಿ ಎಲ್ಲ ದರ ನೋಡಲು | Type *all* for all rates"
    )


def _handle_apmc_followup(phone: str, message: str, session: dict) -> str:
    msg = message.lower().strip()

    if msg in ("all", "ಎಲ್ಲ", "ಎಲ್ಲಾ"):
        result = fetch_apmc_rates()
        update_session(phone, {"current_flow": None})
        return format_rates_message(result) + "\n\n_ಮತ್ತೊಂದು ಪ್ರಶ್ನೆ ಇದ್ದರೆ ಕೇಳಿ | Ask me anything else!_"

    # Match crop alias
    crop = None
    for alias in CROP_ALIASES:
        if alias in msg:
            crop = alias
            break
    if not crop:
        crop = msg

    result = fetch_apmc_rates(commodity=crop)
    update_session(phone, {"current_flow": None})
    return format_rates_message(result, commodity=crop) + (
        "\n\n🌾 ಬೇರೆ ಬೆಳೆ ದರ ಬೇಕೇ? | Need another crop's rate? Type the crop name."
    )


# ─────────────────────────────────────────────
# SCHEME FLOW — shows menu
# ─────────────────────────────────────────────

def _start_scheme_flow(phone: str, message: str, session: dict) -> str:
    update_session(phone, {"current_flow": "scheme_info_flow"})
    return (
        "🏛️ *ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು | Government Schemes*\n"
        "Mandya ಜಿಲ್ಲೆ ರೈತರಿಗಾಗಿ | For Mandya Farmers\n\n"
        "ಯಾವ ಯೋಜನೆ ಬಗ್ಗೆ ತಿಳಿಯಲು ಬಯಸುತ್ತೀರಿ?\n"
        "Which scheme do you want to know about?\n\n"
        "1️⃣ 💰 *PM-KISAN* — ₹6,000/year income support\n"
        "2️⃣ 🌧️ *PMFBY* — Crop Insurance\n"
        "3️⃣ 💳 *KCC* — Kisan Credit Card (4% loan)\n"
        "4️⃣ 🎋 *Raita Siri* — Sugarcane growers' scheme\n"
        "5️⃣ 🧪 *Soil Health Card* — Free soil testing\n"
        "6️⃣ 💧 *Drip/Sprinkler Subsidy* — 50-90% off\n\n"
        "ಸಂಖ್ಯೆ ಅಥವಾ ಯೋಜನೆ ಹೆಸರು ಕಳಿಸಿ | Send number or scheme name"
    )


def _handle_scheme_info_flow(phone: str, message: str, session: dict) -> str:
    """Handle scheme selection from the scheme menu."""
    msg = message.strip().lower()
    scheme_map = {
        "1": "pm_kisan", "2": "pmfby", "3": "kcc",
        "4": "karnataka_raita_siri", "5": "soil_health_card", "6": "drip_sprinkler",
    }
    scheme_id = scheme_map.get(msg) or _detect_scheme_from_msg(message)

    if not scheme_id:
        return (
            "ದಯವಿಟ್ಟು 1-6 ಸಂಖ್ಯೆ ಕಳಿಸಿ | Please send a number 1-6\n"
            "1-PM-KISAN | 2-PMFBY | 3-KCC | 4-Raita Siri | 5-Soil Card | 6-Drip"
        )

    update_session(phone, {"current_flow": None})
    return _format_scheme_info(scheme_id)


def _handle_scheme_direct(phone: str, message: str, session: dict) -> str:
    """Farmer typed a scheme name directly — show info immediately."""
    scheme_id = _detect_scheme_from_msg(message)
    if scheme_id:
        update_session(phone, {"current_flow": None})
        return _format_scheme_info(scheme_id)
    return _start_scheme_flow(phone, message, session)


def _format_scheme_info(scheme_id: str) -> str:
    scheme = SCHEMES.get(scheme_id)
    if not scheme:
        return "ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ | Information not available."

    contacts = "\n".join(
        f"  📞 {c['name']}: *{c['number']}*"
        for c in scheme.get("contacts", [])
    )
    docs = " | ".join(scheme.get("documents", [])[:4])
    how_to = scheme.get("how_to_apply", "")
    how_to_kn = scheme.get("how_to_apply_kn", "")

    msg = (
        f"🏛️ *{scheme['name']}*\n"
        f"_{scheme.get('kannada_name', '')}_\n\n"
        f"💰 *ಪ್ರಯೋಜನ | Benefit:*\n{scheme.get('benefit', '')}\n"
        f"_{scheme.get('benefit_kn', '')}_\n\n"
    )
    if how_to:
        msg += f"📋 *ಅರ್ಜಿ ವಿಧಾನ | How to Apply:*\n{how_to}\n\n"
    if docs:
        msg += f"📄 *ದಾಖಲೆಗಳು | Documents:* {docs}\n\n"
    msg += f"📞 *ಸಂಪರ್ಕ | Contacts:*\n{contacts}\n\n"
    msg += (
        "_ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಲು 'eligibility' ಟೈಪ್ ಮಾಡಿ_\n"
        "_Type 'eligibility' to check if you qualify_"
    )
    return msg


# ─────────────────────────────────────────────
# ELIGIBILITY FLOW
# ─────────────────────────────────────────────

def _start_eligibility_selection(phone: str, message: str, session: dict) -> str:
    scheme_id = _detect_scheme_from_msg(message)
    if scheme_id:
        return _begin_eligibility_questions(phone, scheme_id)

    update_session(phone, {
        "current_flow": "scheme_eligibility_flow",
        "eligibility_step": "select_scheme"
    })
    return (
        "✅ *ಅರ್ಹತೆ ತಿಳಿಯಿರಿ | Check Your Eligibility*\n\n"
        "ಯಾವ ಯೋಜನೆ / ಸಾಲಕ್ಕೆ ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಬೇಕು?\n"
        "Which scheme/loan to check?\n\n"
        "1️⃣ PM-KISAN\n"
        "2️⃣ PMFBY (Crop Insurance)\n"
        "3️⃣ KCC (Kisan Credit Card)\n"
        "4️⃣ Karnataka Raita Siri\n"
        "5️⃣ Soil Health Card\n"
        "6️⃣ Drip/Sprinkler Subsidy\n"
        "7️⃣ Agriculture Bank Loan\n\n"
        "ಸಂಖ್ಯೆ ಕಳಿಸಿ | Send a number (1-7)"
    )


def _begin_eligibility_questions(phone: str, scheme_id: str) -> str:
    scheme = SCHEMES.get(scheme_id) or BANK_LOANS.get(scheme_id)
    if not scheme:
        return "❌ Scheme not found. Type *menu* to start over."

    questions = scheme.get("eligibility_questions", [])
    if not questions:
        return (
            f"✅ *{scheme['name']}*\n\n"
            f"Everyone with agricultural land in Mandya is eligible — it's FREE!\n"
            f"ಭೂಮಿ ಇರುವ ಎಲ್ಲ ರೈತರಿಗೂ ಅರ್ಹತೆ ಇದೆ — ಉಚಿತ!\n\n"
            f"📞 {scheme.get('contacts', [{}])[0].get('number', 'Contact agriculture office')}"
        )

    update_session(phone, {
        "current_flow": "scheme_eligibility_flow",
        "eligibility_step": "questioning",
        "scheme_id": scheme_id,
        "question_index": 0,
        "answers": {}
    })

    q_key, q_text = questions[0]
    return (
        f"✅ *{scheme['name']}* — ಅರ್ಹತೆ ಪರಿಶೀಲನೆ | Eligibility Check\n\n"
        f"ನಾನು ಕೆಲವು ಪ್ರಶ್ನೆ ಕೇಳುತ್ತೇನೆ — ದಯವಿಟ್ಟು ಉತ್ತರಿಸಿ.\n"
        f"I'll ask a few questions — please answer them.\n\n"
        f"❓ *{q_text}*\n\n"
        f"_ಹೌದು/Yes ಅಥವಾ ಇಲ್ಲ/No ಎಂದು ಉತ್ತರಿಸಿ_"
    )


def _handle_eligibility_flow(phone: str, message: str, session: dict) -> str:
    step = session.get("eligibility_step", "select_scheme")

    if step == "select_scheme":
        scheme_map = {
            "1": "pm_kisan", "2": "pmfby", "3": "kcc",
            "4": "karnataka_raita_siri", "5": "soil_health_card",
            "6": "drip_sprinkler", "7": "crop_loan"
        }
        scheme_id = scheme_map.get(message.strip()) or _detect_scheme_from_msg(message)
        if not scheme_id:
            return "ದಯವಿಟ್ಟು 1-7 ಸಂಖ್ಯೆ ಕಳಿಸಿ | Please send a number 1-7"
        return _begin_eligibility_questions(phone, scheme_id)

    elif step == "questioning":
        scheme_id = session.get("scheme_id")
        scheme = SCHEMES.get(scheme_id) or BANK_LOANS.get(scheme_id)
        if not scheme:
            clear_session(phone)
            return "ದಯವಿಟ್ಟು *menu* ಟೈಪ್ ಮಾಡಿ | Type *menu* to start over"

        questions = scheme.get("eligibility_questions", [])
        q_index = session.get("question_index", 0)
        answers = session.get("answers", {})

        # Save current answer (whatever they typed — yes/no or free text like "sugarcane and 1 acre")
        if q_index < len(questions):
            q_key, _ = questions[q_index]
            answers[q_key] = message.strip()

        q_index += 1
        session["question_index"] = q_index
        session["answers"] = answers

        if q_index < len(questions):
            save_session(phone, session)
            q_key, q_text = questions[q_index]
            return f"❓ *{q_text}*\n\n_ಹೌದು/Yes ಅಥವಾ ಇಲ್ಲ/No ಅಥವಾ ನಿಮ್ಮ ಉತ್ತರ ಟೈಪ್ ಮಾಡಿ_"
        else:
            result = check_scheme_eligibility(scheme_id, answers)
            clear_session(phone)
            status_emoji = "✅" if result["eligible"] else "❌"
            status_text = (
                "ಅರ್ಹರಾಗಿದ್ದೀರಿ | You ARE Eligible!"
                if result["eligible"] else
                "ಈ ಸಮಯದಲ್ಲಿ ಅರ್ಹರಲ್ಲ | Not eligible right now"
            )
            reasons = "\n".join(result["reasons"])
            return (
                f"🔍 *{scheme['name']}* — ಫಲಿತಾಂಶ | Result\n\n"
                f"{status_emoji} *{status_text}*\n\n"
                f"{reasons}\n\n"
                f"📋 *ಮುಂದಿನ ಹಂತ | Next Steps:*\n{result['next_steps']}\n\n"
                f"_'eligibility' ಟೈಪ್ ಮಾಡಿ ಇನ್ನೊಂದು ಪರಿಶೀಲಿಸಲು_\n"
                f"_Type 'eligibility' to check another scheme_"
            )

    return _call_gemini(phone, message, session)


# ─────────────────────────────────────────────
# LOAN FLOW — shows loan menu with bank details
# ─────────────────────────────────────────────

def _start_loan_flow(phone: str, message: str, session: dict) -> str:
    update_session(phone, {"current_flow": "loan_flow"})
    return (
        "🏦 *ಕೃಷಿ ಸಾಲ ಮಾಹಿತಿ | Farm Loan Information*\n"
        "Mandya ಜಿಲ್ಲೆ | For Mandya Farmers\n\n"
        "ನಿಮಗೆ ಯಾವ ಸಾಲ ಬಗ್ಗೆ ತಿಳಿಯಬೇಕು?\n"
        "Which loan do you want to know about?\n\n"
        "1️⃣ 💳 *KCC* — Kisan Credit Card (4% interest)\n"
        "2️⃣ 🚜 *Agriculture Term Loan* — Equipment / Land / Irrigation\n"
        "3️⃣ 📋 *Short Term Crop Loan* — Seasonal expenses\n\n"
        "🏦 *Mandya Banks that offer farm loans:*\n"
        "• SBI Mandya: *08232-222-001*\n"
        "• Canara Bank Mandya: *08232-222-118*\n"
        "• Karnataka Grameena Bank: *08232-225-700*\n"
        "• Syndicate Bank Mandya: *08232-222-500*\n\n"
        "ಸಂಖ್ಯೆ ಕಳಿಸಿ (1-3) | Send number (1-3)"
    )


def _handle_loan_flow(phone: str, message: str, session: dict) -> str:
    msg = message.strip().lower()
    loan_map = {"1": "kcc", "2": "agriculture_term_loan", "3": "crop_loan"}
    loan_id = loan_map.get(msg)

    if not loan_id:
        if "kcc" in msg or "kisan credit" in msg:
            loan_id = "kcc"
        elif "term" in msg or "equipment" in msg or "tractor" in msg:
            loan_id = "agriculture_term_loan"
        elif "crop" in msg or "short" in msg or "ಬೆಳೆ" in message:
            loan_id = "crop_loan"

    if loan_id:
        update_session(phone, {"current_flow": None})
        return _format_loan_info(loan_id)

    return (
        "ದಯವಿಟ್ಟು 1, 2, ಅಥವಾ 3 ಕಳಿಸಿ | Please send 1, 2, or 3\n"
        "1-KCC | 2-Term Loan | 3-Crop Loan"
    )


def _format_loan_info(loan_id: str) -> str:
    loan = BANK_LOANS.get(loan_id) or SCHEMES.get(loan_id)
    if not loan:
        return "Loan information not found. ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ."

    contacts = "\n".join(
        f"  📞 {c['name']}: *{c['number']}*"
        for c in loan.get("contacts", [])
    )
    docs = " | ".join(loan.get("documents", [])[:4])
    docs_kn = " | ".join(loan.get("documents_kn", [])[:4])
    how_to = loan.get("how_to_apply", "")
    how_to_kn = loan.get("how_to_apply_kn", "")

    msg = (
        f"🏦 *{loan['name']}*\n"
        f"_{loan.get('kannada_name', '')}_\n\n"
        f"💰 *ಪ್ರಯೋಜನ | Benefit:*\n{loan.get('benefit', '')}\n"
        f"_{loan.get('benefit_kn', '')}_\n\n"
    )
    if loan.get("interest_rate"):
        msg += f"📊 *ಬಡ್ಡಿ ದರ | Interest Rate:* {loan['interest_rate']}\n\n"
    if how_to:
        msg += f"📋 *ಅರ್ಜಿ ವಿಧಾನ | How to Apply:*\n{how_to}\n\n{how_to_kn}\n\n"
    if docs:
        msg += f"📄 *ದಾಖಲೆಗಳು | Documents:*\n{docs}\n{docs_kn}\n\n"
    msg += f"📞 *ಸಂಪರ್ಕ | Contacts:*\n{contacts}\n\n"
    msg += (
        "_ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಲು 'eligibility' ಟೈಪ್ ಮಾಡಿ_\n"
        "_Type 'eligibility' to check if you qualify_"
    )
    return msg


# ─────────────────────────────────────────────
# FERTILIZER FLOW
# ─────────────────────────────────────────────

def _start_fertilizer_flow(phone: str, message: str, session: dict) -> str:
    msg_lower = message.lower()

    # Check pending_crop from clarify step
    pending = session.get("pending_crop", "")
    if message.strip() == "2" and pending:
        crop_key = _match_crop_key(pending)
        if crop_key:
            update_session(phone, {"current_flow": None, "pending_crop": ""})
            return _give_crop_advice(crop_key)

    # Check if a specific crop is mentioned in message
    for key in CROP_ADVICE:
        if key in msg_lower or CROP_ADVICE[key]["kannada"] in message:
            update_session(phone, {"current_flow": None})
            return _give_crop_advice(key)

    update_session(phone, {"current_flow": "fertilizer_flow"})
    return (
        "🌿 *ಬೆಳೆ ಮತ್ತು ಗೊಬ್ಬರ ಸಲಹೆ | Crop & Fertilizer Advice*\n\n"
        "ನೀವು ಯಾವ ಬೆಳೆ ಬೆಳೆಯುತ್ತಿದ್ದೀರಿ?\n"
        "Which crop are you growing?\n\n"
        "1️⃣ 🎋 ಕಬ್ಬು | Sugarcane\n"
        "2️⃣ 🌾 ಭತ್ತ | Paddy\n"
        "3️⃣ 🌿 ರಾಗಿ | Ragi\n"
        "4️⃣ 🍅 ಟೊಮೆಟೊ | Tomato\n"
        "5️⃣ 🥥 ತೆಂಗಿನಕಾಯಿ | Coconut\n"
        "6️⃣ 🍌 ಬಾಳೆ | Banana\n\n"
        "ಸಂಖ್ಯೆ ಅಥವಾ ಬೆಳೆ ಹೆಸರು ಕಳಿಸಿ | Send number or crop name"
    )


def _handle_fertilizer_flow(phone: str, message: str, session: dict) -> str:
    msg = message.lower().strip()
    crop_map = {
        "1": "sugarcane", "2": "paddy", "3": "ragi",
        "4": "tomato", "5": "coconut", "6": "banana",
        "ಕಬ್ಬು": "sugarcane", "ಭತ್ತ": "paddy", "ರಾಗಿ": "ragi",
        "ಟೊಮೆಟೊ": "tomato", "ತೆಂಗಿನಕಾಯಿ": "coconut", "ಬಾಳೆ": "banana",
    }
    crop_key = crop_map.get(msg)
    if not crop_key:
        for key in CROP_ADVICE:
            if key in msg:
                crop_key = key
                break

    if crop_key and crop_key in CROP_ADVICE:
        update_session(phone, {"current_flow": None})
        return _give_crop_advice(crop_key)

    return (
        "ಕ್ಷಮಿಸಿ, ಬೆಳೆ ಗುರುತಿಸಲಾಗಲಿಲ್ಲ | Sorry, crop not recognised.\n\n"
        "1-ಕಬ್ಬು | 2-ಭತ್ತ | 3-ರಾಗಿ | 4-ಟೊಮೆಟೊ | 5-ತೆಂಗಿನಕಾಯಿ | 6-ಬಾಳೆ"
    )


def _match_crop_key(text: str) -> str:
    text = text.lower()
    for key in CROP_ADVICE:
        if key in text:
            return key
    if "ಕಬ್ಬು" in text:
        return "sugarcane"
    if "ಭತ್ತ" in text:
        return "paddy"
    if "ರಾಗಿ" in text:
        return "ragi"
    if "ಟೊಮೆಟೊ" in text:
        return "tomato"
    return None


def _give_crop_advice(crop_key: str) -> str:
    advice = CROP_ADVICE[crop_key]
    shop = random.choice(FERTILIZER_SHOPS)

    lines = [
        f"🌿 *{crop_key.title()} ({advice['kannada']}) — ಕೃಷಿ ಸಲಹೆ | Farming Advice*\n",
        f"🌱 *ತಳಿಗಳು | Varieties:*\n{', '.join(advice['varieties'])}\n",
        f"📅 *ಋತು | Season:*\n{advice['season']}\n{advice['season_kn']}\n",
        "🧪 *ಗೊಬ್ಬರ | Fertilizer:*",
    ]
    for stage, rec in advice["fertilizer"].items():
        kn_rec = advice["fertilizer_kn"].get(stage, "")
        lines.append(f"• {rec}")
        if kn_rec:
            lines.append(f"  _{kn_rec}_")

    lines.append(f"\n💧 *ನೀರಾವರಿ | Irrigation:*\n{advice['water']}\n{advice['water_kn']}")
    lines.append(f"\n🐛 *ರೋಗ/ಕೀಟ | Issues:*\n{advice['common_issues']}")
    lines.append(
        f"\n🛒 *ಹತ್ತಿರದ ಅಂಗಡಿ | Nearby Shop:*\n"
        f"📍 *{shop['name']}*, {shop['location']}\n"
        f"📞 *{shop['contact']}*\n"
        f"Products: {', '.join(shop['products'][:3])}"
    )
    lines.append(
        f"\n\n❓ ನಿಮ್ಮ ಬೆಳೆ ಈಗ ಯಾವ ಹಂತದಲ್ಲಿದೆ?\n"
        f"(ಬಿತ್ತನೆ / ಬೆಳವಣಿಗೆ / ಹೂ ಬಿಡುವ / ಕಟಾವು)\n"
        f"Which growth stage is your crop at?\n"
        f"(Sowing / Growing / Flowering / Harvest)"
    )
    return "\n".join(lines)


# ─────────────────────────────────────────────
# GEMINI FALLBACK
# ─────────────────────────────────────────────

def _call_gemini(phone: str, message: str, session: dict) -> str:
    history = session.get("gemini_history", [])
    contents = []
    for turn in history[-16:]:
        contents.append(types.Content(
            role=turn["role"],
            parts=[types.Part(text=turn["text"])]
        ))
    contents.append(types.Content(
        role="user",
        parts=[types.Part(text=message)]
    ))

    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=500,
                temperature=0.7,
            )
        )
        reply = response.text.strip()
    except Exception as e:
        print(f"[Gemini] Error: {e}")
        reply = (
            "🙏 ಕ್ಷಮಿಸಿ, ತಾಂತ್ರಿಕ ತೊಂದರೆ. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ.\n"
            "Sorry, technical issue. Please try again.\n"
            "📞 Mandya Agriculture: *08232-222-666*"
        )

    history.append({"role": "user",  "text": message})
    history.append({"role": "model", "text": reply})
    update_session(phone, {"gemini_history": history, "current_flow": None})
    return reply


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _detect_scheme_from_msg(message: str) -> str:
    msg = message.lower()
    if "pm kisan" in msg or "pmkisan" in msg or "6000" in msg or "kisan samman" in msg:
        return "pm_kisan"
    if "pmfby" in msg or "fasal bima" in msg or "crop insurance" in msg or "ಬೆಳೆ ವಿಮೆ" in message:
        return "pmfby"
    if "kcc" in msg or "kisan credit" in msg:
        return "kcc"
    if "raita siri" in msg or "ರೈತ ಸಿರಿ" in message or "raitha siri" in msg:
        return "karnataka_raita_siri"
    if "soil health" in msg or "soil card" in msg or "ಮಣ್ಣು ಆರೋಗ್ಯ" in message:
        return "soil_health_card"
    if "drip" in msg or "sprinkler" in msg or "ಹನಿ ನೀರಾವರಿ" in message:
        return "drip_sprinkler"
    return None

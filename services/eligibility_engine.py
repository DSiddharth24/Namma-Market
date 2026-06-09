"""
Eligibility Engine
Checks farmer eligibility for schemes and bank loans based on collected Q&A answers.
Returns structured eligibility result with reasons and next steps.
"""

from data.schemes import SCHEMES, BANK_LOANS


def check_scheme_eligibility(scheme_id: str, answers: dict) -> dict:
    """
    Check eligibility for a specific scheme.
    answers: dict of {question_key: answer_string}
    Returns: {eligible: bool, reasons: list, next_steps: str}
    """
    if scheme_id == "pm_kisan":
        return _check_pm_kisan(answers)
    elif scheme_id == "pmfby":
        return _check_pmfby(answers)
    elif scheme_id == "kcc":
        return _check_kcc(answers)
    elif scheme_id == "karnataka_raita_siri":
        return _check_raita_siri(answers)
    elif scheme_id == "soil_health_card":
        return _check_soil_health_card(answers)
    elif scheme_id == "drip_sprinkler":
        return _check_drip_sprinkler(answers)
    elif scheme_id in ("agriculture_term_loan", "crop_loan"):
        return _check_bank_loan(scheme_id, answers)
    return {"eligible": None, "reasons": ["Eligibility check not available for this scheme."], "next_steps": ""}


def _yes(val: str) -> bool:
    if not val:
        return False
    return val.lower().strip() in ("yes", "ಹೌದು", "y", "ha", "houdhu", "haan", "han", "1", "true")


def _no(val: str) -> bool:
    if not val:
        return False
    return val.lower().strip() in ("no", "ಇಲ್ಲ", "n", "illa", "nahi", "naa", "0", "false")


def _check_pm_kisan(answers: dict) -> dict:
    reasons = []
    eligible = True

    land_owner = answers.get("land_owner", "")
    income_tax = answers.get("income_tax", "")
    govt_employee = answers.get("govt_employee", "")
    aadhaar = answers.get("aadhaar", "")

    if not _yes(land_owner):
        eligible = False
        reasons.append(
            "❌ You must own agricultural land registered in your name.\n"
            "   ❌ ನಿಮ್ಮ ಹೆಸರಿನಲ್ಲಿ ಕೃಷಿ ಭೂಮಿ ಇರಬೇಕು."
        )
    else:
        reasons.append("✅ Land ownership: Eligible\n   ✅ ಭೂ ಮಾಲೀಕತ್ವ: ಅರ್ಹ")

    if _yes(income_tax):
        eligible = False
        reasons.append(
            "❌ Income tax payers are not eligible for PM-KISAN.\n"
            "   ❌ ಆದಾಯ ತೆರಿಗೆ ತೆರುವವರು ಈ ಯೋಜನೆಗೆ ಅರ್ಹರಲ್ಲ."
        )
    else:
        reasons.append("✅ Not an income tax payer: Eligible\n   ✅ ಆದಾಯ ತೆರಿಗೆ ಇಲ್ಲ: ಅರ್ಹ")

    if _yes(govt_employee):
        eligible = False
        reasons.append(
            "❌ Government employees/pensioners above ₹10,000/month are not eligible.\n"
            "   ❌ ಸರ್ಕಾರಿ ನೌಕರರು/ನಿವೃತ್ತರು ಅರ್ಹರಲ್ಲ."
        )
    else:
        reasons.append("✅ Not a government employee: Eligible\n   ✅ ಸರ್ಕಾರಿ ನೌಕರ ಅಲ್ಲ: ಅರ್ಹ")

    if not _yes(aadhaar):
        reasons.append(
            "⚠️ Aadhaar card mandatory. Get it linked to your bank first.\n"
            "   ⚠️ ಆಧಾರ್ ಕಾರ್ಡ್ ಬ್ಯಾಂಕ್‌ಗೆ ಲಿಂಕ್ ಮಾಡಿಸಿ."
        )
        if eligible:
            eligible = True  # Still eligible, just needs Aadhaar
    else:
        reasons.append("✅ Aadhaar ready: Good to go\n   ✅ ಆಧಾರ್ ಸಿದ್ಧ: ಅರ್ಜಿ ಮಾಡಬಹುದು")

    next_steps = (
        "1. Visit pmkisan.gov.in or nearest CSC centre in Mandya\n"
        "2. Carry: Aadhaar + RTC (Pahani) + Bank Passbook\n"
        "3. Complete eKYC for activation\n"
        "📞 Helpline: *155261* or *1800-11-5526*\n\n"
        "1. pmkisan.gov.in ಅಥವಾ Mandya CSC ಕೇಂದ್ರಕ್ಕೆ ಹೋಗಿ\n"
        "2. ತರಬೇಕಾದ ದಾಖಲೆ: ಆಧಾರ್ + RTC + ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್\n"
        "📞 ಸಹಾಯವಾಣಿ: *155261*"
    ) if eligible else (
        "You may not qualify right now. Please consult:\n"
        "📞 Mandya District Agriculture Office: *08232-222-666*\n\n"
        "ನೀವು ಈಗ ಅರ್ಹರಾಗದಿರಬಹುದು. ಸಂಪರ್ಕಿಸಿ:\n"
        "📞 ಮಂಡ್ಯ ಜಿಲ್ಲಾ ಕೃಷಿ ಇಲಾಖೆ: *08232-222-666*"
    )

    return {"eligible": eligible, "reasons": reasons, "next_steps": next_steps}


def _check_pmfby(answers: dict) -> dict:
    reasons = []
    eligible = True

    aadhaar = answers.get("aadhaar", "")

    if not _yes(aadhaar):
        eligible = False
        reasons.append("❌ Aadhaar is mandatory for PMFBY.\n   ❌ ಆಧಾರ್ ಕಾರ್ಡ್ ಅನಿವಾರ್ಯ.")
    else:
        reasons.append("✅ Aadhaar available\n   ✅ ಆಧಾರ್ ಇದೆ")

    crop = answers.get("crop_type", "")
    if crop:
        reasons.append(f"✅ Crop '{crop}' — eligible if it is a notified crop in Mandya\n   ✅ ಬೆಳೆ ಅಧಿಸೂಚಿತ ಆಗಿದ್ದರೆ ಅರ್ಹ")
    else:
        reasons.append("ℹ️ Crop type not specified — most major Mandya crops (paddy, ragi, sugarcane) are covered")

    kcc = answers.get("kcc_loan", "")
    if _yes(kcc):
        reasons.append("ℹ️ KCC holder: PMFBY enrollment is compulsory for you (done automatically by bank)")
    else:
        reasons.append("ℹ️ No KCC: You can voluntarily enroll at bank or CSC before crop season deadline")

    next_steps = (
        "1. Visit your bank or CSC before crop season starts\n"
        "2. Pay premium (2% for Kharif, 1.5% for Rabi)\n"
        "3. For claims, call within 72 hours of loss\n"
        "📞 Helpline: *14447* | *1800-116-515*\n"
        "🌐 pmfby.gov.in\n\n"
        "1. ಬೆಳೆ ಋತು ಮೊದಲು ಬ್ಯಾಂಕ್ / CSC ಗೆ ಹೋಗಿ\n"
        "2. ಪ್ರೀಮಿಯಂ ಪಾವತಿಸಿ\n"
        "3. ನಷ್ಟ ಆದ 72 ಗಂಟೆಯೊಳಗೆ ಕ್ಲೇಮ್ ಮಾಡಿ\n"
        "📞 *14447*"
    )

    return {"eligible": eligible, "reasons": reasons, "next_steps": next_steps}


def _check_kcc(answers: dict) -> dict:
    reasons = []
    eligible = True

    age_str = answers.get("age", "")
    land_area = answers.get("land_area", "")
    existing_loan = answers.get("existing_loan", "")
    bank_account = answers.get("bank_account", "")

    # Age check
    try:
        age = int("".join(filter(str.isdigit, age_str)))
        if age < 18:
            eligible = False
            reasons.append(f"❌ Age {age} — must be at least 18 years\n   ❌ ವಯಸ್ಸು 18 ವರ್ಷ ತುಂಬಿರಬೇಕು")
        elif age > 75:
            reasons.append(f"⚠️ Age {age} — a co-borrower (family member) may be required\n   ⚠️ 75 ವರ್ಷ ಮೀರಿದ್ದರೆ ಜಂಟಿ ಸಾಲಗಾರ ಬೇಕು")
        else:
            reasons.append(f"✅ Age {age}: Eligible\n   ✅ ವಯಸ್ಸು {age}: ಅರ್ಹ")
    except Exception:
        reasons.append("ℹ️ Age not confirmed — please check with bank")

    # Land area
    if land_area:
        reasons.append(f"✅ Land: {land_area} acres — eligible for KCC\n   ✅ ಜಮೀನು {land_area} ಎಕರೆ — KCC ಪಡೆಯಬಹುದು")
    else:
        reasons.append("ℹ️ Land area not specified — any land area qualifies")

    # Existing loans
    if _yes(existing_loan):
        reasons.append("⚠️ Existing loans may affect KCC limit. Bank will assess credit history.\n   ⚠️ ಇರುವ ಸಾಲ KCC ಮಿತಿ ಕಡಿಮೆ ಮಾಡಬಹುದು")
    else:
        reasons.append("✅ No existing loans: Better chance of higher KCC limit\n   ✅ ಸಾಲ ಇಲ್ಲ: ಹೆಚ್ಚಿನ KCC ಮಿತಿ ಪಡೆಯಬಹುದು")

    if not _yes(bank_account):
        reasons.append("⚠️ Bank account needed. Open one before applying.\n   ⚠️ ಮೊದಲು ಬ್ಯಾಂಕ್ ಖಾತೆ ತೆರೆಯಿರಿ")

    next_steps = (
        "🏦 Visit any of these Mandya banks with documents:\n"
        "• SBI Mandya: *08232-222-001*\n"
        "• Canara Bank Mandya: *08232-222-118*\n"
        "• Karnataka Grameena Bank: *08232-225-700*\n\n"
        "📄 Documents needed:\n"
        "Aadhaar + PAN + Land records (RTC) + 2 photos + Bank account\n\n"
        "ℹ️ KCC limit = 1.5× your crop production cost per acre × acres"
    )

    return {"eligible": eligible, "reasons": reasons, "next_steps": next_steps}


def _check_raita_siri(answers: dict) -> dict:
    crop = answers.get("crop", "")
    mill = answers.get("mill", "")
    reasons = []
    eligible = True

    if not _yes(crop) and "sugarcane" not in crop.lower() and "ಕಬ್ಬು" not in crop:
        eligible = False
        reasons.append("❌ This scheme is only for sugarcane growers.\n   ❌ ಈ ಯೋಜನೆ ಕಬ್ಬು ಬೆಳೆಗಾರರಿಗೆ ಮಾತ್ರ.")
    else:
        reasons.append("✅ You grow sugarcane: Eligible\n   ✅ ಕಬ್ಬು ಬೆಳೆಯುತ್ತೀರಿ: ಅರ್ಹ")

    if mill:
        reasons.append(f"✅ Mill: {mill}\n   ✅ ಕಾರ್ಖಾನೆ ನೋಂದಾವಣೆ ಅಗತ್ಯ — ಮಂಡ್ಯ ಸಕ್ಕರೆ ಕಾರ್ಖಾನೆಯಲ್ಲಿ ನೋಂದಾಯಿಸಿ")

    next_steps = (
        "📞 Mandya Sugar Factory (Mys Sugar): *08232-222-200*\n"
        "📞 Karnataka Sugar Directorate: *080-2220-0501*\n\n"
        "ನಿಮ್ಮ ಸಕ್ಕರೆ ಕಾರ್ಖಾನೆಯಲ್ಲಿ ರೈತ ಸಿರಿ ಬಗ್ಗೆ ಕೇಳಿ"
    )
    return {"eligible": eligible, "reasons": reasons, "next_steps": next_steps}


def _check_soil_health_card(answers: dict) -> dict:
    land = answers.get("land", "")
    if _yes(land):
        return {
            "eligible": True,
            "reasons": ["✅ Any farmer with agricultural land is eligible — it's FREE!\n   ✅ ಎಲ್ಲ ರೈತರಿಗೂ ಅರ್ಹತೆ — ಉಚಿತ!"],
            "next_steps": (
                "📞 Soil Testing Lab, Mandya: *08232-222-888*\n"
                "📞 Agriculture Dept Mandya: *08232-222-666*\n"
                "🌐 soilhealth.dac.gov.in\n\n"
                "ಮಣ್ಣು ಮಾದರಿ ಸಂಗ್ರಹಿಸಿ ಕೃಷಿ ಇಲಾಖೆಗೆ ಕೊಡಿ — 15-20 ದಿನದಲ್ಲಿ ಕಾರ್ಡ್ ಸಿಗುತ್ತದೆ"
            )
        }
    return {
        "eligible": False,
        "reasons": ["❌ Agricultural land required.\n   ❌ ಕೃಷಿ ಭೂಮಿ ಬೇಕು."],
        "next_steps": ""
    }


def _check_drip_sprinkler(answers: dict) -> dict:
    land_area = answers.get("land_area", "")
    water_source = answers.get("water_source", "")
    category = answers.get("category", "")
    reasons = []
    eligible = True

    try:
        area = float("".join(c for c in land_area if c.isdigit() or c == "."))
        if area < 0.5:
            eligible = False
            reasons.append("❌ Minimum 0.5 acre land required\n   ❌ ಕನಿಷ್ಟ 0.5 ಎಕರೆ ಭೂಮಿ ಬೇಕು")
        else:
            reasons.append(f"✅ Land: {area} acres — Eligible\n   ✅ ಜಮೀನು {area} ಎಕರೆ: ಅರ್ಹ")
    except Exception:
        reasons.append("ℹ️ Land area not confirmed")

    if _yes(water_source):
        reasons.append("✅ Water source available: Required for drip system\n   ✅ ನೀರಿನ ಮೂಲ ಇದೆ: ಅಗತ್ಯ")
    else:
        eligible = False
        reasons.append("❌ Water source (borewell/canal) required\n   ❌ ಬೋರ್‌ವೆಲ್ ಅಥವಾ ನಾಲೆ ಇರಬೇಕು")

    sc_st = _yes(category) or "sc" in category.lower() or "st" in category.lower()
    subsidy = "90%" if sc_st else "50%"
    reasons.append(f"💰 Your subsidy: *{subsidy}* on equipment cost\n   💰 ನಿಮ್ಮ ಸಹಾಯಧನ: *{subsidy}*")

    next_steps = (
        f"Your subsidy rate: *{subsidy}*\n"
        "📞 Horticulture Dept Mandya: *08232-222-777*\n"
        "📞 Agriculture Dept Mandya: *08232-222-666*\n\n"
        f"ನಿಮ್ಮ ಸಹಾಯಧನ: *{subsidy}*\n"
        "📞 ತೋಟಗಾರಿಕೆ ಇಲಾಖೆ ಮಂಡ್ಯ: *08232-222-777*"
    )
    return {"eligible": eligible, "reasons": reasons, "next_steps": next_steps}


def _check_bank_loan(loan_id: str, answers: dict) -> dict:
    reasons = []
    eligible = True

    land_area = answers.get("land_area", "")
    existing_loan = answers.get("existing_loan", "")

    if land_area:
        reasons.append(f"✅ Land: {land_area} acres — Eligible for loan\n   ✅ ಜಮೀನು {land_area} ಎಕರೆ: ಸಾಲಕ್ಕೆ ಅರ್ಹ")

    if _yes(existing_loan):
        reasons.append("⚠️ Existing loan: Bank will check CIBIL score. Maintain timely repayments.\n   ⚠️ ಇರುವ ಸಾಲ: CIBIL ಸ್ಕೋರ್ ತಪಾಸಣೆ ಆಗುತ್ತದೆ")
    else:
        reasons.append("✅ No existing loan: Clean slate — higher chance of approval\n   ✅ ಸಾಲ ಇಲ್ಲ: ಅನುಮೋದನೆ ಸಾಧ್ಯತೆ ಹೆಚ್ಚು")

    next_steps = (
        "🏦 Contact any Mandya bank:\n"
        "• SBI Mandya: *08232-222-001*\n"
        "• Canara Bank Mandya: *08232-222-118*\n"
        "• Karnataka Grameena Bank: *08232-225-700*\n"
        "• NABARD Karnataka: *080-2228-0581*\n\n"
        "📄 Documents: Aadhaar + PAN + Land RTC + 2 photos + Bank passbook\n\n"
        "ಯಾವುದೇ ಮಂಡ್ಯ ಬ್ಯಾಂಕ್‌ಗೆ ಹೋಗಿ ಮೇಲಿನ ದಾಖಲೆಗಳೊಂದಿಗೆ"
    )
    return {"eligible": eligible, "reasons": reasons, "next_steps": next_steps}

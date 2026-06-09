"""
Government Schemes Data for Mandya District Farmers
Includes Central and Karnataka State schemes with official contacts.
"""

SCHEMES = {
    "pm_kisan": {
        "id": "pm_kisan",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "kannada_name": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ",
        "benefit": "₹6,000 per year in 3 installments of ₹2,000 directly to bank account",
        "benefit_kn": "ವರ್ಷಕ್ಕೆ ₹6,000 — ₹2,000 × 3 ಕಂತುಗಳಲ್ಲಿ ನೇರ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ",
        "eligibility": {
            "land": "Must own agricultural land (any size)",
            "income": "Not applicable to income tax payers, govt. employees, pensioners (>₹10,000/month)",
            "registration": "Aadhaar mandatory, bank account required",
        },
        "eligibility_questions": [
            ("land_owner", "Do you own agricultural land in your name? (ನಿಮ್ಮ ಹೆಸರಿನಲ್ಲಿ ಕೃಷಿ ಭೂಮಿ ಇದೆಯೇ?)"),
            ("income_tax", "Do you or your family pay income tax? (ನೀವು ಆದಾಯ ತೆರಿಗೆ ತೆರುತ್ತೀರಾ?)"),
            ("govt_employee", "Are you or your spouse a government employee/pensioner? (ಸರ್ಕಾರಿ ಉದ್ಯೋಗಿ/ನಿವೃತ್ತರಿದ್ದೀರಾ?)"),
            ("aadhaar", "Do you have an Aadhaar card linked to your bank account? (ಆಧಾರ್ ಕಾರ್ಡ್ ಬ್ಯಾಂಕ್‌ಗೆ ಲಿಂಕ್ ಆಗಿದೆಯೇ?)"),
        ],
        "how_to_apply": (
            "1. Visit pmkisan.gov.in or nearest CSC center\n"
            "2. Register with Aadhaar + land records (RTC/Pahani)\n"
            "3. Complete eKYC at CSC or via OTP\n"
            "4. Verify status on pmkisan.gov.in"
        ),
        "how_to_apply_kn": (
            "1. pmkisan.gov.in ಅಥವಾ ಹತ್ತಿರದ CSC ಕೇಂದ್ರಕ್ಕೆ ಹೋಗಿ\n"
            "2. ಆಧಾರ್ + ಭೂಮಿ ದಾಖಲೆ (RTC/ಪಹಣಿ) ಸಲ್ಲಿಸಿ\n"
            "3. CSC ನಲ್ಲಿ ಅಥವಾ OTP ಮೂಲಕ eKYC ಮಾಡಿ\n"
            "4. pmkisan.gov.in ನಲ್ಲಿ ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಿ"
        ),
        "contacts": [
            {"name": "PM-KISAN Helpline", "number": "155261"},
            {"name": "PM-KISAN Toll Free", "number": "1800-11-5526"},
            {"name": "Mandya District Agriculture Office", "number": "08232-222-666"},
            {"name": "Official Website", "number": "pmkisan.gov.in"},
        ],
        "documents": ["Aadhaar Card", "Bank Passbook", "Land Records (RTC/7-12)", "Mobile number"],
        "documents_kn": ["ಆಧಾರ್ ಕಾರ್ಡ್", "ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್", "ಭೂಮಿ ದಾಖಲೆ (RTC)", "ಮೊಬೈಲ್ ನಂಬರ್"],
    },

    "pmfby": {
        "id": "pmfby",
        "name": "PMFBY (Pradhan Mantri Fasal Bima Yojana) - Crop Insurance",
        "kannada_name": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ - ಬೆಳೆ ವಿಮೆ",
        "benefit": "Crop insurance for losses due to natural calamities, pests, drought",
        "benefit_kn": "ನೈಸರ್ಗಿಕ ವಿಪತ್ತು, ಕೀಟ, ಬರದಿಂದ ಬೆಳೆ ನಷ್ಟಕ್ಕೆ ಪರಿಹಾರ",
        "premium": {
            "kharif": "2% of sum insured for Kharif crops",
            "rabi": "1.5% for Rabi crops",
            "horticulture": "5% for commercial/horticultural crops",
        },
        "premium_kn": {
            "kharif": "ಖರೀಫ್ ಬೆಳೆಗಳಿಗೆ ವಿಮಾ ಮೊತ್ತದ 2%",
            "rabi": "ರಬಿ ಬೆಳೆಗಳಿಗೆ 1.5%",
            "horticulture": "ತೋಟಗಾರಿಕೆ ಬೆಳೆಗಳಿಗೆ 5%",
        },
        "eligibility": {
            "land": "All farmers (owners and sharecroppers/tenants) growing notified crops",
            "kcc": "Compulsory for KCC loan holders; optional for others",
        },
        "eligibility_questions": [
            ("crop_type", "Which crop are you growing? (ನೀವು ಯಾವ ಬೆಳೆ ಬೆಳೆಯುತ್ತಿದ್ದೀರಿ?)"),
            ("land_owner", "Are you land owner or tenant farmer? (ಭೂ ಮಾಲೀಕರೇ ಅಥವಾ ಗೇಣಿದಾರರೇ?)"),
            ("kcc_loan", "Do you have a KCC/crop loan? (KCC ಸಾಲ ಇದೆಯೇ?)"),
            ("aadhaar", "Do you have Aadhaar card? (ಆಧಾರ್ ಕಾರ್ಡ್ ಇದೆಯೇ?)"),
        ],
        "how_to_apply": (
            "1. Apply through nearest bank or Common Service Centre (CSC)\n"
            "2. Deadline: 2 weeks before crop sowing season\n"
            "3. Claim within 72 hours of crop loss via helpline or app\n"
            "4. Check status: pmfby.gov.in"
        ),
        "how_to_apply_kn": (
            "1. ಹತ್ತಿರದ ಬ್ಯಾಂಕ್ ಅಥವಾ CSC ಕೇಂದ್ರದಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ\n"
            "2. ಬಿತ್ತನೆ ಮೊದಲು 2 ವಾರದೊಳಗೆ ನೋಂದಾಯಿಸಿ\n"
            "3. ಬೆಳೆ ನಷ್ಟದ 72 ಗಂಟೆಯೊಳಗೆ ಕ್ಲೇಮ್ ಮಾಡಿ\n"
            "4. pmfby.gov.in ನಲ್ಲಿ ಸ್ಥಿತಿ ತಿಳಿಯಿರಿ"
        ),
        "contacts": [
            {"name": "PMFBY Helpline", "number": "14447"},
            {"name": "Agriculture Insurance Company (AIC)", "number": "1800-116-515"},
            {"name": "Mandya District Agriculture Office", "number": "08232-222-666"},
            {"name": "Official Website", "number": "pmfby.gov.in"},
        ],
        "documents": ["Aadhaar Card", "Bank account details", "Land records (RTC)", "Sowing certificate"],
        "documents_kn": ["ಆಧಾರ್ ಕಾರ್ಡ್", "ಬ್ಯಾಂಕ್ ವಿವರ", "ಭೂಮಿ ದಾಖಲೆ (RTC)", "ಬಿತ್ತನೆ ಪ್ರಮಾಣಪತ್ರ"],
    },

    "kcc": {
        "id": "kcc",
        "name": "KCC - Kisan Credit Card",
        "kannada_name": "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ (KCC)",
        "benefit": "Revolving crop loan up to ₹3 lakh at 4% interest (after govt. subsidy) for crop and allied activities",
        "benefit_kn": "ಸರ್ಕಾರ ಸಬ್ಸಿಡಿ ನಂತರ 4% ಬಡ್ಡಿ ದರದಲ್ಲಿ ₹3 ಲಕ್ಷದವರೆಗೆ ಬೆಳೆ ಸಾಲ",
        "eligibility": {
            "land": "All farmers (individual/joint/tenant/sharecroppers)",
            "age": "18 to 75 years (co-borrower if above 60)",
            "crops": "Any crop grown in notified area",
        },
        "eligibility_questions": [
            ("age", "What is your age? (ನಿಮ್ಮ ವಯಸ್ಸು ಎಷ್ಟು?)"),
            ("land_area", "How much land do you own/cultivate (in acres)? (ನೀವು ಎಷ್ಟು ಎಕರೆ ಜಮೀನು ಹೊಂದಿದ್ದೀರಿ?)"),
            ("existing_loan", "Do you have any existing loans with banks? (ಈಗಾಗಲೇ ಬ್ಯಾಂಕ್ ಸಾಲ ಇದೆಯೇ?)"),
            ("bank_account", "Do you have a bank account? (ಬ್ಯಾಂಕ್ ಖಾತೆ ಇದೆಯೇ?)"),
        ],
        "how_to_apply": (
            "1. Visit nearest SBI, Canara Bank, or Karnataka Grameena Bank branch\n"
            "2. Submit application with land records and Aadhaar\n"
            "3. Bank officer inspects land and sanctions loan\n"
            "4. KCC issued within 14 working days"
        ),
        "how_to_apply_kn": (
            "1. ಹತ್ತಿರದ SBI, ಕೆನರಾ ಬ್ಯಾಂಕ್ ಅಥವಾ ಕರ್ನಾಟಕ ಗ್ರಾಮೀಣ ಬ್ಯಾಂಕ್‌ಗೆ ಹೋಗಿ\n"
            "2. ಭೂಮಿ ದಾಖಲೆ ಮತ್ತು ಆಧಾರ್ ಸಲ್ಲಿಸಿ\n"
            "3. ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿ ಜಮೀನು ತಪಾಸಣೆ ಮಾಡುತ್ತಾರೆ\n"
            "4. 14 ಕೆಲಸದ ದಿನಗಳಲ್ಲಿ KCC ನೀಡಲಾಗುತ್ತದೆ"
        ),
        "contacts": [
            {"name": "SBI Mandya Branch", "number": "08232-222-001"},
            {"name": "Canara Bank Mandya", "number": "08232-222-118"},
            {"name": "Karnataka Grameena Bank (KGB) Mandya", "number": "08232-225-700"},
            {"name": "NABARD Karnataka", "number": "080-2228-0581"},
            {"name": "KCC Helpline", "number": "1800-180-1551"},
        ],
        "documents": ["Aadhaar Card", "PAN Card", "Land records (RTC/7-12/8A)", "2 passport photos", "Bank account"],
        "documents_kn": ["ಆಧಾರ್ ಕಾರ್ಡ್", "PAN ಕಾರ್ಡ್", "ಭೂಮಿ ದಾಖಲೆ (RTC)", "2 ಪಾಸ್‌ಪೋರ್ಟ್ ಫೋಟೋ", "ಬ್ಯಾಂಕ್ ಖಾತೆ"],
    },

    "karnataka_raita_siri": {
        "id": "karnataka_raita_siri",
        "name": "Karnataka Raita Siri Scheme",
        "kannada_name": "ಕರ್ನಾಟಕ ರೈತ ಸಿರಿ ಯೋಜನೆ",
        "benefit": "Incentive payment to sugarcane growers in addition to factory payment",
        "benefit_kn": "ಕಬ್ಬು ಬೆಳೆಗಾರರಿಗೆ ಕಾರ್ಖಾನೆ ಬೆಲೆ ಜೊತೆಗೆ ಹೆಚ್ಚುವರಿ 장ower",
        "eligibility": {
            "crop": "Sugarcane growers supplying to licensed sugar mills in Karnataka",
            "land": "Registered cane grower with the sugar factory",
        },
        "eligibility_questions": [
            ("crop", "Are you growing sugarcane? (ನೀವು ಕಬ್ಬು ಬೆಳೆಯುತ್ತಿದ್ದೀರಾ?)"),
            ("mill", "Which sugar mill do you supply to? (ಯಾವ ಸಕ್ಕರೆ ಕಾರ್ಖಾನೆಗೆ ಕಬ್ಬು ಕೊಡುತ್ತೀರಿ?)"),
        ],
        "contacts": [
            {"name": "Mandya Sugar Factory (Mys Sugar)", "number": "08232-222-200"},
            {"name": "Karnataka Sugar Directorate", "number": "080-2220-0501"},
            {"name": "Karnataka Agriculture Dept Mandya", "number": "08232-222-666"},
        ],
        "documents": ["Cane supply receipts", "Land records", "Bank account"],
        "documents_kn": ["ಕಬ್ಬು ಪೂರೈಕೆ ರಸೀತಿ", "ಭೂಮಿ ದಾಖಲೆ", "ಬ್ಯಾಂಕ್ ಖಾತೆ"],
    },

    "soil_health_card": {
        "id": "soil_health_card",
        "name": "Soil Health Card Scheme",
        "kannada_name": "ಮಣ್ಣು ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಯೋಜನೆ",
        "benefit": "Free soil testing and personalized fertilizer recommendation card every 2 years",
        "benefit_kn": "ಉಚಿತ ಮಣ್ಣು ಪರೀಕ್ಷೆ ಮತ್ತು ಗೊಬ್ಬರ ಶಿಫಾರಸು ಕಾರ್ಡ್ — ಪ್ರತಿ 2 ವರ್ಷಕ್ಕೊಮ್ಮೆ ಉಚಿತ",
        "eligibility": {
            "land": "Any farmer owning or cultivating agricultural land",
        },
        "eligibility_questions": [
            ("land", "Do you have agricultural land? (ನಿಮ್ಮ ಬಳಿ ಕೃಷಿ ಭೂಮಿ ಇದೆಯೇ?)"),
        ],
        "contacts": [
            {"name": "Soil Testing Lab, Mandya", "number": "08232-222-888"},
            {"name": "Agriculture Dept. Mandya", "number": "08232-222-666"},
            {"name": "Soil Health Card Portal", "number": "soilhealth.dac.gov.in"},
        ],
        "documents": ["Land records", "Aadhaar Card"],
        "documents_kn": ["ಭೂಮಿ ದಾಖಲೆ", "ಆಧಾರ್ ಕಾರ್ಡ್"],
    },

    "drip_sprinkler": {
        "id": "drip_sprinkler",
        "name": "PMKSY - Drip / Sprinkler Irrigation Subsidy",
        "kannada_name": "ಹನಿ ನೀರಾವರಿ / ತುಂತುರು ನೀರಾವರಿ ಸಹಾಯಧನ (PMKSY)",
        "benefit": "50-90% subsidy on drip and sprinkler irrigation equipment for SC/ST farmers. 50% for general farmers.",
        "benefit_kn": "SC/ST ರೈತರಿಗೆ 90%, ಸಾಮಾನ್ಯ ರೈತರಿಗೆ 50% ಸಹಾಯಧನ",
        "eligibility": {
            "land": "Minimum 0.5 acre land",
            "water": "Must have a water source (borewell, canal, tank)",
        },
        "eligibility_questions": [
            ("land_area", "How many acres of land do you have? (ಎಷ್ಟು ಎಕರೆ ಭೂಮಿ ಇದೆ?)"),
            ("water_source", "Do you have a water source (borewell/canal)? (ಬೋರ್‌ವೆಲ್ ಅಥವಾ ನಾಲೆ ಇದೆಯೇ?)"),
            ("category", "Are you SC/ST farmer? (ನೀವು SC/ST ರೈತರೇ?)"),
        ],
        "contacts": [
            {"name": "Horticulture Dept Mandya", "number": "08232-222-777"},
            {"name": "Agriculture Dept Mandya", "number": "08232-222-666"},
        ],
        "documents": ["Aadhaar", "Land records", "Water source proof", "Caste certificate (if SC/ST)"],
        "documents_kn": ["ಆಧಾರ್", "ಭೂಮಿ ದಾಖಲೆ", "ನೀರಿನ ಮೂಲ ದಾಖಲೆ", "ಜಾತಿ ಪ್ರಮಾಣಪತ್ರ (SC/ST ಆಗಿದ್ದರೆ)"],
    },
}


BANK_LOANS = {
    "agriculture_term_loan": {
        "id": "agriculture_term_loan",
        "name": "Agriculture Term Loan (Land Development, Equipment, Irrigation)",
        "kannada_name": "ಕೃಷಿ ಮುದ್ದತಿ ಸಾಲ",
        "benefit": "Long-term loan for land development, farm equipment, irrigation structures. Up to ₹20 lakh.",
        "benefit_kn": "ಭೂ ಅಭಿವೃದ್ಧಿ, ಕೃಷಿ ಯಂತ್ರ, ನೀರಾವರಿ ನಿರ್ಮಾಣಕ್ಕೆ ₹20 ಲಕ್ಷದವರೆಗೆ ದೀರ್ಘಾವಧಿ ಸಾಲ",
        "interest_rate": "7-9% per annum (with interest subvention from govt.)",
        "repayment": "3-7 years depending on loan purpose",
        "eligibility_questions": [
            ("purpose", "What is the loan for? (Equipment / Land Development / Irrigation?) (ಸಾಲ ಯಾವ ಉದ್ದೇಶಕ್ಕೆ?)"),
            ("land_area", "How many acres of land do you own? (ಎಷ್ಟು ಎಕರೆ ಜಮೀನು ಇದೆ?)"),
            ("existing_loan", "Do you have any existing bank loans? (ಈಗಾಗಲೇ ಸಾಲ ಇದೆಯೇ?)"),
        ],
        "contacts": [
            {"name": "SBI Mandya Main Branch", "number": "08232-222-001"},
            {"name": "Canara Bank Mandya", "number": "08232-222-118"},
            {"name": "Karnataka Grameena Bank (KGB)", "number": "08232-225-700"},
            {"name": "NABARD Karnataka Helpline", "number": "080-2228-0581"},
        ],
    },
    "crop_loan": {
        "id": "crop_loan",
        "name": "Short Term Crop Loan (Kharif / Rabi)",
        "kannada_name": "ಅಲ್ಪಾವಧಿ ಬೆಳೆ ಸಾಲ",
        "benefit": "Crop loan up to ₹3 lakh at 4% effective interest (after 3% interest subvention by Govt.)",
        "benefit_kn": "₹3 ಲಕ್ಷದವರೆಗೆ ಸರ್ಕಾರ ಸಬ್ಸಿಡಿ ನಂತರ 4% ಬಡ್ಡಿ ದರದಲ್ಲಿ ಬೆಳೆ ಸಾಲ",
        "interest_rate": "Effective 4% (7% minus 3% Govt. interest subvention for timely repayment)",
        "eligibility_questions": [
            ("land_area", "How much land do you cultivate? (ಎಷ್ಟು ಎಕರೆ ಭೂಮಿ ಬೇಸಾಯ ಮಾಡುತ್ತೀರಿ?)"),
            ("crop", "Which crop are you planning to grow? (ಯಾವ ಬೆಳೆ ಬೆಳೆಯಲು ಯೋಜಿಸಿದ್ದೀರಿ?)"),
            ("kcc", "Do you already have a KCC (Kisan Credit Card)? (KCC ಇದೆಯೇ?)"),
        ],
        "contacts": [
            {"name": "SBI Mandya Main Branch", "number": "08232-222-001"},
            {"name": "Canara Bank Mandya", "number": "08232-222-118"},
            {"name": "Karnataka Grameena Bank (KGB) Mandya", "number": "08232-225-700"},
            {"name": "Syndicate Bank Mandya", "number": "08232-222-500"},
        ],
    },
}
